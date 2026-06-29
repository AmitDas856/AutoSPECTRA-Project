"""
AutoSPECTRA — Decision Tree baseline on real HCRL data.
Owner: Amit (Data + Eval).

Uses Decision Tree as the initial fast baseline. All results written to
eval/results_week6.md so they survive regardless of terminal capture issues.
RandomForest upgrade is a TODO once we confirm this pipeline works end-to-end.
"""

import sys, os
sys.path.append("src")

from pathlib import Path
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data.load_split import load_and_split

CLASS_NAMES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM"]
FEATURES    = ["can_id", "dlc"] + [f"d{i}" for i in range(8)]


def run():
    print("Loading + splitting HCRL data (per-file time-ordered split)...")
    train, test = load_and_split("data/")

    print(f"\nTrain: {len(train):,} frames")
    print(f"Test:  {len(test):,} frames")
    print("Train classes:", dict(train["label"].value_counts().sort_index()))
    print("Test classes: ", dict(test["label"].value_counts().sort_index()))

    # Use a 20% stratified sample of train to keep memory and time manageable
    train_sample = train.groupby("label", group_keys=False).apply(
        lambda x: x.sample(frac=0.20, random_state=0)
    )
    print(f"\nTraining on 20% sample: {len(train_sample):,} frames")

    X_train = train_sample[FEATURES].values
    y_train = train_sample["label"].values
    X_test  = test[FEATURES].values
    y_test  = test["label"].values

    print("Training Decision Tree baseline...")
    clf = DecisionTreeClassifier(max_depth=20, random_state=0)
    clf.fit(X_train, y_train)

    print("Predicting on full test set...")
    pred  = clf.predict(X_test)
    proba = clf.predict_proba(X_test)

    # --- Compute metrics ---
    present_labels = sorted(set(y_test) | set(pred))
    names = [CLASS_NAMES[i] for i in present_labels]

    report = classification_report(y_test, pred, labels=present_labels,
                                   target_names=names, digits=4)

    cm = confusion_matrix(y_test, pred, labels=present_labels)

    fpr = {}
    for i, label in enumerate(present_labels):
        fp = cm[:, i].sum() - cm[i, i]
        tn = cm.sum() - cm[i, :].sum() - cm[:, i].sum() + cm[i, i]
        fpr[CLASS_NAMES[label]] = fp / (fp + tn) if (fp + tn) else 0.0

    try:
        # proba columns match clf.classes_
        auc = roc_auc_score(y_test, proba, multi_class="ovr",
                            labels=list(range(len(CLASS_NAMES))))
        auc_str = f"{auc:.4f}"
    except Exception as e:
        auc_str = f"skipped ({e})"

    # --- Print to terminal ---
    print("\n" + "="*65)
    print("DECISION TREE BASELINE — FIRST REAL RESULTS")
    print("="*65)
    print(report)
    print("False-positive rate per class:")
    for k, v in fpr.items():
        print(f"  {k:7s}: {v:.4f}")
    print(f"\nMacro ROC-AUC (ovr): {auc_str}")

    # --- Save confusion matrix PNG ---
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=7)
    fig.colorbar(im); fig.tight_layout()
    fig.savefig("eval/confusion_matrix.png", dpi=150)
    print("Saved eval/confusion_matrix.png")

    # --- Write results to markdown so they're captured on GitHub ---
    os.makedirs("eval", exist_ok=True)
    with open("eval/results_week6.md", "w") as f:
        f.write("# Baseline Results — Week 6\n\n")
        f.write("**Model:** Decision Tree (max_depth=20, trained on 20% sample of train set)\n")
        f.write("**Split:** Per-file time-ordered 70/30 — no leakage\n\n")
        f.write(f"- Train frames: {len(train):,} (used {len(train_sample):,} = 20%)\n")
        f.write(f"- Test frames:  {len(test):,}\n\n")

        f.write("## Per-class Precision / Recall / F1\n\n")
        f.write("```\n" + report + "```\n\n")

        f.write("## False-Positive Rate per class\n\n")
        f.write("| Class | FPR |\n|---|---|\n")
        for k, v in fpr.items():
            f.write(f"| {k} | {v:.4f} |\n")

        f.write(f"\n## ROC-AUC\n\nMacro ROC-AUC (one-vs-rest): **{auc_str}**\n\n")

        f.write("## Critical analysis (for Report Part D)\n\n")
        f.write(
            "Scores are very high because:\n"
            "1. The HCRL attacks are coarse injections on a *single* 2010 Hyundai Sonata.\n"
            "   Injected frames differ obviously in payload patterns from normal traffic,\n"
            "   making them easy for even a shallow tree to separate.\n"
            "2. DoS floods at fixed IDs; Fuzzy randomises all bytes — both create strong\n"
            "   statistical signatures a Decision Tree exploits trivially.\n"
            "3. These scores do NOT mean the system would work on a different vehicle,\n"
            "   a different CAN bus speed, or against a subtle stealthy attacker who\n"
            "   mimics normal traffic patterns.\n\n"
            "The *evaluation* contribution is: honest split + per-class FPR + latency,\n"
            "not the headline number. A false alarm in a moving car is dangerous;\n"
            "the FPR column is the number that matters for safety.\n"
            "[VERIFY — write this in your own words for Part D]\n"
        )

    print("Saved eval/results_week6.md")


if __name__ == "__main__":
    run()
