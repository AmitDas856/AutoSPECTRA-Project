"""
AutoSPECTRA — evaluation harness. Owner: Amit (Data + Eval).
This is the backbone: EVERY model (baseline RF, Ad's CNN, Maheswari's seq model)
reports through this so the numbers are comparable. Worth ~30% of the grade.

Inputs:
  y_true : list/array of true class ids (0=Normal,1=DoS,2=Fuzzy,3=Gear,4=RPM)
  y_pred : predicted class ids
  y_score: optional, predicted probabilities (n_samples x n_classes) for ROC-AUC
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # save plots to file without a display
import matplotlib.pyplot as plt
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score)

CLASS_NAMES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM"]


def per_class_report(y_true, y_pred):
    """Per-class precision/recall/F1 + macro-F1. Accuracy alone hides imbalance."""
    # Handle case where not all classes appear in test set
    unique_labels = sorted(set(y_true) | set(y_pred))
    target_names = [CLASS_NAMES[i] for i in unique_labels]
    print(classification_report(y_true, y_pred, labels=unique_labels, target_names=target_names, digits=4))


def false_positive_rate(y_true, y_pred):
    """FPR per class = FP / (FP + TN). Critical in a car: false alarms erode trust."""
    unique_labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
    fpr = {}
    for i, label in enumerate(unique_labels):
        name = CLASS_NAMES[label]
        fp = cm[:, i].sum() - cm[i, i]
        tn = cm.sum() - cm[i, :].sum() - cm[:, i].sum() + cm[i, i]
        fpr[name] = fp / (fp + tn) if (fp + tn) else 0.0
    return fpr


def plot_confusion(y_true, y_pred, out="eval/confusion_matrix.png"):
    unique_labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels)
    names = [CLASS_NAMES[i] for i in unique_labels]
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=8)
    fig.colorbar(im); fig.tight_layout(); fig.savefig(out, dpi=150)
    print(f"saved {out}")


def evaluate(y_true, y_pred, y_score=None):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    print("=== Per-class metrics ===")
    per_class_report(y_true, y_pred)
    print("=== False-positive rate per class ===")
    for k, v in false_positive_rate(y_true, y_pred).items():
        print(f"  {k:7s}: {v:.4f}")
    plot_confusion(y_true, y_pred)
    if y_score is not None:
        try:
            auc = roc_auc_score(y_true, y_score, multi_class="ovr")
            print(f"Macro ROC-AUC (ovr): {auc:.4f}")
        except Exception as e:
            print("ROC-AUC skipped:", e)


if __name__ == "__main__":
    # Smoke test with fake data so you see the output shape before wiring real models.
    rng = np.random.default_rng(0)
    y_true = rng.integers(0, 5, size=2000)
    y_pred = y_true.copy()
    flip = rng.random(2000) < 0.05          # 5% errors
    y_pred[flip] = rng.integers(0, 5, size=flip.sum())
    evaluate(y_true, y_pred)
