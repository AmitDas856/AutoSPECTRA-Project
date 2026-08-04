"""Tabular baselines on the real HCRL data: Decision Tree and RandomForest.
Amit (Data + Eval)."""

# Both models are trained on the same 20% stratified sample of the train split
# and tested on the FULL held-out test split, so the comparison is fair.
# Everything is written to eval/results_week6.md so the evidence is on GitHub.

import sys
import os
sys.path.append("src")
sys.path.append("eval")

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, roc_auc_score

from data.load_split import load_and_split
from run_eval import (CLASS_NAMES, false_positive_rate, plot_confusion,
                      detection_latency)

FEATURES = ["can_id", "dlc"] + [f"d{i}" for i in range(8)]


def sample_train(train, frac=0.20):
    # Take the same fraction from every class so the sample keeps the class
    # balance of the full training set (stratified sample).
    sample_parts = []
    for cls in sorted(train["label"].unique()):
        part = train[train["label"] == cls]
        sample_parts.append(part.sample(frac=frac, random_state=0))
    return pd.concat(sample_parts)


def run_model(name, clf, X_train, y_train, X_test, y_test, ts_test):
    # Train one model and collect every metric the report needs.
    print(f"\n--- {name} ---")
    print("fitting...")
    clf.fit(X_train, y_train)
    print("predicting on full test set...")
    pred = clf.predict(X_test)
    proba = clf.predict_proba(X_test)

    present = sorted(set(y_test.tolist()) | set(pred.tolist()))
    names = [CLASS_NAMES[i] for i in present]
    report = classification_report(y_test, pred, labels=present,
                                   target_names=names, digits=4)
    macro_f1 = f1_score(y_test, pred, average="macro")
    fpr = false_positive_rate(y_test, pred)
    try:
        auc = f"{roc_auc_score(y_test, proba, multi_class='ovr'):.4f}"
    except Exception as e:
        auc = f"skipped ({e})"
    latency = detection_latency(ts_test, y_test, pred)
    plot_confusion(y_test, pred, out=f"eval/confusion_{name}.png")

    print(report)
    print("latency:", latency)
    result = {
        "report": report,
        "macro_f1": macro_f1,
        "fpr": fpr,
        "auc": auc,
        "latency": latency,
    }
    return result


def main():
    print("Loading + splitting HCRL data (per-file time-ordered split)...")
    train, test = load_and_split("data/")
    print(f"Train {len(train):,} | Test {len(test):,}")

    train_sample = sample_train(train)
    X_train = train_sample[FEATURES].values
    y_train = train_sample["label"].values
    X_test = test[FEATURES].values
    y_test = test["label"].values
    ts_test = test["timestamp"].values
    print(f"Fitting on {len(train_sample):,} frames (20% stratified sample)")

    results = {}
    dt = DecisionTreeClassifier(max_depth=20, random_state=0)
    results["DecisionTree"] = run_model("DecisionTree", dt, X_train, y_train,
                                        X_test, y_test, ts_test)
    rf = RandomForestClassifier(n_estimators=50, max_depth=20, n_jobs=4,
                                random_state=0)
    results["RandomForest"] = run_model("RandomForest", rf, X_train, y_train,
                                        X_test, y_test, ts_test)

    # Write the results file. This is the evidence for Report Part D.
    # encoding="utf-8" matters on Windows: the default is cp1252 and the
    # script crashes on characters like the arrow in the latency line.
    os.makedirs("eval", exist_ok=True)
    with open("eval/results_week6.md", "w", encoding="utf-8") as f:
        f.write("# Baseline Results — Week 6 (tabular models)\n\n")
        f.write("**Split:** per-file time-ordered 70/30, leakage assert passes per file.\n")
        f.write(f"**Train:** {len(train):,} frames (models fit on 20% stratified "
                f"sample = {len(train_sample):,}). **Test:** {len(test):,} frames "
                f"(full held-out tail, all 5 classes).\n\n")

        f.write("## Model comparison (frame-level, full test set)\n\n")
        f.write("| Model | Macro-F1 | ROC-AUC (ovr) | Worst-class FPR |\n|---|---|---|---|\n")
        for name in results:
            r = results[name]
            worst_fpr = max(r["fpr"].values())
            f.write(f"| {name} | {r['macro_f1']:.4f} | {r['auc']} | {worst_fpr:.5f} |\n")

        for name in results:
            r = results[name]
            f.write(f"\n## {name}\n\n```\n{r['report']}```\n\n")
            fpr_parts = []
            for k, v in r["fpr"].items():
                fpr_parts.append(f"{k} {v:.5f}")
            f.write("**False-positive rate per class:** ")
            f.write(", ".join(fpr_parts) + "\n\n")
            f.write("**Detection latency** (episode = burst of attack frames with "
                    "<1s gaps; latency = attack onset → first correctly-flagged frame):\n\n")
            f.write("| Class | Episodes | Detected | Median ms | Max ms | Median frames |\n")
            f.write("|---|---|---|---|---|---|\n")
            for cls, d in r["latency"].items():
                f.write(f"| {cls} | {d['episodes']} | {d['detected']} | "
                        f"{d['median_ms']:.2f} | {d['max_ms']:.2f} | {d['median_frames']} |\n")
            f.write(f"\nConfusion matrix: `eval/confusion_{name}.png`\n")

        f.write(
            "\n## Critical analysis (notes for Report Part D — write in own words)\n\n"
            "- Near-perfect scores are EXPECTED on this dataset, not impressive: the\n"
            "  HCRL attacks are coarse injections on a single 2010 Hyundai Sonata.\n"
            "  DoS floods a fixed CAN ID (0x000) and Fuzzy randomises whole payloads —\n"
            "  both leave signatures a shallow tree separates trivially.\n"
            "- The comparison DT vs RF therefore shows near-identical headline numbers;\n"
            "  the informative columns are FPR (false alarms erode driver trust) and\n"
            "  detection latency (an IDS that flags after the crash is useless).\n"
            "- Latency here is measured per attack EPISODE, strict correct-class flag.\n"
            "- These results say nothing about a different vehicle, bus load, or a\n"
            "  stealthy attacker that mimics normal traffic. Single-vehicle bias is\n"
            "  the headline limitation for Part D.\n"
        )
    print("\nSaved eval/results_week6.md")


if __name__ == "__main__":
    main()
