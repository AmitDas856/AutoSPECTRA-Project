"""Train the SeqLSTM on the real HCRL data. Owner: Maheswari (Sequence).
Run from the repo root:  python src/train_seq.py

This deliberately mirrors train_cnn.py so the two models are compared fairly:
the same per-file time-ordered split, the same non-overlapping windows, the
same capped training sample, and the same evaluation harness. The only thing
that changes is the model — an LSTM reading the sequence instead of a CNN
reading an image. Keeping everything else identical is what makes the
comparison table honest.

Windowing rules (same as the CNN, and they matter for the viva):
  - windows are built per capture file, so a window never spans two files
  - train windows come only from the train part, test windows only from test,
    so nothing straddles the 70/30 time cut
  - a window's label is the attack class if ANY frame inside it is injected,
    else Normal (blunt but standard for window-level IDS; state it in the report)
"""

import sys
import os

sys.path.append("src")

import numpy as np
import torch
import torch.nn as nn

from seq_model import SeqLSTM, normalise_window, WINDOW, N_FEATURES
from data.load_split import load_and_split

FEATURES   = ["can_id"] + [f"d{i}" for i in range(8)]   # 9 features per frame
CAP_ATTACK = 6000     # max train windows per attack class (matches the CNN run)
CAP_NORMAL = 12000    # max Normal train windows
EPOCHS     = 3
BATCH      = 256
SEED       = 0


def make_windows(df):
    # Chop one time-sorted stream into non-overlapping WINDOW-frame windows.
    # Returns X (n, WINDOW, 9), y (n,) window labels, t_end (n,) end timestamps.
    # End timestamp is when the detector could actually decide.
    n = (len(df) // WINDOW) * WINDOW
    if n == 0:
        return (np.empty((0, WINDOW, len(FEATURES)), dtype="float32"),
                np.empty((0,), dtype="int64"), np.empty((0,), dtype="float64"))
    feats  = df[FEATURES].values[:n].reshape(-1, WINDOW, len(FEATURES))
    labels = df["label"].values[:n].reshape(-1, WINDOW)
    times  = df["timestamp"].values[:n].reshape(-1, WINDOW)
    # max = "any attack frame present"; each file has one attack class so there
    # are no mixed-attack windows to worry about.
    y = labels.max(axis=1)
    return feats.astype("float32"), y.astype("int64"), times[:, -1]


def encode(feats):
    # Per-window 0..1 normalisation, no image step — the LSTM reads the
    # sequence directly. Shape stays (n, WINDOW, n_features).
    return np.stack([normalise_window(w) for w in feats]).astype("float32")


def main():
    torch.manual_seed(SEED)
    rng = np.random.default_rng(SEED)

    print("Loading per-file split...")
    parts = load_and_split("data/", return_parts=True)

    tr_X, tr_y, te_X, te_y, te_t = [], [], [], [], []
    for attack, tr, te in parts:
        X, y, _ = make_windows(tr)
        tr_X.append(X); tr_y.append(y)
        X, y, t = make_windows(te)
        te_X.append(X); te_y.append(y); te_t.append(t)
    tr_X = np.concatenate(tr_X); tr_y = np.concatenate(tr_y)
    te_X = np.concatenate(te_X); te_y = np.concatenate(te_y); te_t = np.concatenate(te_t)
    print(f"Windows: {len(tr_y):,} train | {len(te_y):,} test (size {WINDOW})")

    # Cap train windows per class so 3 CPU epochs stay quick. Test is NOT
    # capped — full coverage or the numbers lie.
    keep = []
    for cls in np.unique(tr_y):
        idx = np.where(tr_y == cls)[0]
        cap = CAP_NORMAL if cls == 0 else CAP_ATTACK
        if len(idx) > cap:
            idx = rng.choice(idx, size=cap, replace=False)
        keep.append(idx)
    keep = np.concatenate(keep)
    rng.shuffle(keep)
    tr_X, tr_y = tr_X[keep], tr_y[keep]
    print(f"Capped train windows: {len(tr_y):,}",
          dict(zip(*np.unique(tr_y, return_counts=True))))

    print("Normalising windows...")
    Xtr = torch.from_numpy(encode(tr_X))
    ytr = torch.from_numpy(tr_y)
    Xte = torch.from_numpy(encode(te_X))

    model = SeqLSTM()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    print(f"Training SeqLSTM: {EPOCHS} epochs, batch {BATCH}, CPU")
    model.train()
    for epoch in range(EPOCHS):
        perm, losses = torch.randperm(len(ytr)), []
        for i in range(0, len(ytr), BATCH):
            b = perm[i:i + BATCH]
            opt.zero_grad()
            loss = loss_fn(model(Xtr[b]), ytr[b])
            loss.backward(); opt.step()
            losses.append(float(loss.detach()))
        print(f"  epoch {epoch + 1}: mean loss {np.mean(losses):.4f}")

    print("Predicting on ALL test windows...")
    model.eval()
    preds, scores = [], []
    with torch.no_grad():
        for i in range(0, len(Xte), 1024):
            logits = model(Xte[i:i + 1024])
            p = torch.softmax(logits, dim=1)
            scores.append(p.numpy()); preds.append(p.argmax(dim=1).numpy())
    pred = np.concatenate(preds); proba = np.concatenate(scores)

    # Report through Amit's harness — one metrics implementation for every model.
    sys.path.append("eval")
    from run_eval import (CLASS_NAMES, false_positive_rate, plot_confusion,
                          detection_latency)
    from sklearn.metrics import classification_report, f1_score, roc_auc_score

    present = sorted(set(te_y.tolist()) | set(pred.tolist()))
    names = [CLASS_NAMES[i] for i in present]
    report = classification_report(te_y, pred, labels=present,
                                   target_names=names, digits=4)
    macro_f1 = f1_score(te_y, pred, average="macro")
    fpr = false_positive_rate(te_y, pred)
    try:
        auc = f"{roc_auc_score(te_y, proba, multi_class='ovr'):.4f}"
    except Exception as e:
        auc = f"skipped ({e})"
    latency = detection_latency(te_t, te_y, pred)
    plot_confusion(te_y, pred, out="eval/confusion_SeqLSTM.png")

    print(report)
    print("FPR:", {k: round(v, 5) for k, v in fpr.items()})
    print("Macro ROC-AUC:", auc)
    print("Latency:", latency)

    # utf-8 explicitly — Windows defaults to cp1252 and mangles the dashes.
    os.makedirs("eval", exist_ok=True)
    with open("eval/results_seq.md", "w", encoding="utf-8") as f:
        f.write("# SeqLSTM Results — CAN window as a sequence -> LSTM (Week 7)\n\n")
        f.write(f"**Unit:** windows of {WINDOW} frames (window = attack if any "
                "injected frame inside). Same split and windowing as the CNN, so "
                "results_cnn.md is the direct comparison.\n\n")
        f.write(f"- Train: {len(ytr):,} windows (capped; {CAP_NORMAL} Normal / "
                f"{CAP_ATTACK} per attack)\n")
        f.write(f"- Test: {len(te_y):,} windows = full held-out tail\n")
        f.write(f"- {EPOCHS} epochs, batch {BATCH}, Adam 1e-3, CPU\n\n")
        f.write(f"## Per-class metrics\n\n```\n{report}\n```\n\n")
        f.write(f"**Macro-F1:** {macro_f1:.4f} | **Macro ROC-AUC (ovr):** {auc}\n\n")
        fpr_parts = [f"{k} {v:.5f}" for k, v in fpr.items()]
        f.write("**FPR per class:** " + ", ".join(fpr_parts) + "\n\n")
        f.write("## Detection latency (window-level)\n\n")
        f.write("| Class | Episodes | Detected | Median ms | Max ms |\n|---|---|---|---|---|\n")
        for cls, d in latency.items():
            f.write(f"| {cls} | {d['episodes']} | {d['detected']} | "
                    f"{d['median_ms']:.2f} | {d['max_ms']:.2f} |\n")
        f.write("\nConfusion matrix: `eval/confusion_SeqLSTM.png`\n")
    print("Saved eval/results_seq.md")


if __name__ == "__main__":
    main()
