"""Evaluation harness. Amit (Data + Eval). Every model reports through this file
so the numbers are comparable: baseline, Ad's CNN, Maheswari's sequence model."""

# The report needs per-class numbers, not just accuracy. Accuracy looks high
# when 95% of the frames are Normal, even if every attack is missed.

import numpy as np
import matplotlib
matplotlib.use("Agg")  # save plots to file, no display window needed
import matplotlib.pyplot as plt
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score)

CLASS_NAMES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM"]


def per_class_report(y_true, y_pred):
    # Precision, recall and F1 for each class plus macro-F1.
    # Not every class always appears in a test slice, so the labels are
    # taken from the data instead of assuming all five are present.
    unique_labels = sorted(set(y_true) | set(y_pred))
    target_names = [CLASS_NAMES[i] for i in unique_labels]
    print(classification_report(y_true, y_pred, labels=unique_labels, target_names=target_names, digits=4))


def false_positive_rate(y_true, y_pred):
    # FPR per class = FP / (FP + TN). This matters in a car: a false alarm
    # while driving erodes trust in the system and could be dangerous.
    unique_labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
    fpr = {}
    for i, label in enumerate(unique_labels):
        name = CLASS_NAMES[label]
        fp = cm[:, i].sum() - cm[i, i]
        tn = cm.sum() - cm[i, :].sum() - cm[:, i].sum() + cm[i, i]
        if (fp + tn) > 0:
            fpr[name] = fp / (fp + tn)
        else:
            fpr[name] = 0.0
    return fpr


def plot_confusion(y_true, y_pred, out="eval/confusion_matrix.png"):
    # Draw the confusion matrix and save it as a PNG for the report.
    unique_labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
    names = [CLASS_NAMES[i] for i in unique_labels]
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=8)
    fig.colorbar(im)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


def detection_latency(timestamps, y_true, y_pred, gap_s=1.0):
    """Detection latency per attack class: how long from the start of an attack
    until the model first flags it with the correct class."""
    # Attack frames are grouped into episodes. A new episode starts when the
    # gap since the previous attack frame of that class is more than gap_s
    # seconds. The latency of an episode is the time from its first frame to
    # the first frame the model labels with the correct attack class. An
    # episode that is never flagged correctly counts as missed.
    #
    # "frames" counts the attack frames seen before the first correct flag.
    # Normal frames in between are not counted.
    #
    # The rows must be sorted by time inside each class. Our per-file split
    # already gives that, because each class comes from one file.
    ts = np.asarray(timestamps, dtype=float)
    yt = np.asarray(y_true)
    yp = np.asarray(y_pred)
    results = {}
    for cls in sorted(set(yt.tolist()) - {0}):
        idx = np.where(yt == cls)[0]
        if len(idx) == 0:
            continue
        t = ts[idx]
        # Positions where the time gap says a new episode begins.
        new_ep = np.where(np.diff(t) > gap_s)[0] + 1
        episodes = np.split(np.arange(len(idx)), new_ep)
        lat_ms = []
        lat_frames = []
        detected = 0
        for ep in episodes:
            ep_rows = idx[ep]
            hit = np.where(yp[ep_rows] == cls)[0]
            if len(hit):
                detected += 1
                lat_ms.append((ts[ep_rows[hit[0]]] - ts[ep_rows[0]]) * 1000.0)
                lat_frames.append(int(hit[0]))
        if lat_ms:
            median_ms = float(np.median(lat_ms))
            max_ms = float(np.max(lat_ms))
            median_frames = int(np.median(lat_frames))
        else:
            median_ms = float("nan")
            max_ms = float("nan")
            median_frames = -1
        results[CLASS_NAMES[cls]] = {
            "episodes": len(episodes),
            "detected": detected,
            "median_ms": median_ms,
            "max_ms": max_ms,
            "median_frames": median_frames,
        }
    return results


def evaluate(y_true, y_pred, y_score=None, out="eval/confusion_matrix.png"):
    # Run the full set of metrics and save the confusion matrix plot.
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    print("=== Per-class metrics ===")
    per_class_report(y_true, y_pred)
    print("=== False-positive rate per class ===")
    for k, v in false_positive_rate(y_true, y_pred).items():
        print(f"  {k:7s}: {v:.4f}")
    plot_confusion(y_true, y_pred, out=out)
    if y_score is not None:
        try:
            auc = roc_auc_score(y_true, y_score, multi_class="ovr")
            print(f"Macro ROC-AUC (ovr): {auc:.4f}")
        except Exception as e:
            print("ROC-AUC skipped:", e)


if __name__ == "__main__":
    # Smoke test with fake labels, to check the output shape before real models.
    rng = np.random.default_rng(0)
    y_true = rng.integers(0, 5, size=2000)
    y_pred = y_true.copy()
    flip = rng.random(2000) < 0.05  # 5% wrong on purpose
    y_pred[flip] = rng.integers(0, 5, size=flip.sum())
    evaluate(y_true, y_pred)
