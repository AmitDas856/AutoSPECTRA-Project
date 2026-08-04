# Evaluation Plan  *(Report Part D · LO3 = **30%** — the single biggest grade lever)*

> 30% of the grade, and the rubric rewards "clear metrics, tables, visualisations" plus critical awareness of limitations. Build the eval harness early and re-run it as the models improve. **The trap:** published Car-Hacking results sit near 0.99 — reporting "99% accuracy" with no critique is a Pass, not a Distinction. The marks are in the *critical* analysis.

## Metrics (report all per-attack-class, not just overall)
- **Precision / Recall / F1 per class** (Normal, DoS, Fuzzy, Spoof, Gear) + macro-F1. Accuracy alone hides class imbalance.
- **Confusion matrix** — which attacks get confused with normal traffic.
- **ROC-AUC** per attack class.
- **False-positive rate** — *critical in a car*: false alarms erode trust and could trigger unsafe driver reactions. Weight this explicitly.
- **Detection latency** — frames (and ms) from attack onset to flag. An IDS that detects after the crash is useless.
- **Model footprint / inference time on CPU** — supports the "runs on a laptop / could run on an ECU" claim.

## Experimental protocol (what becomes tables/plots in the report)
1. **Baseline:** the feature + RandomForest model in `src/can_ids.py` (already runs).
2. **Headline model:** CAN-frames → recurrence/grid **image → CNN** (the CV component).
3. **Comparison:** **LSTM/autoencoder** on the ID/payload sequence (supervised vs unsupervised).
4. **Ablations:** window size, image encoding (recurrence vs grid), feature set → table.
5. **Generalisation (stretch):** train on Car-Hacking, test on **ROAD** → honest cross-dataset numbers.

## ⚠️ Methodology cautions (state these — they earn Distinction marks)
- **Use a time-ordered split, not a random shuffle.** Random splits leak future frames into training and inflate scores. Say you did this.
- **Single vehicle (2010 Hyundai)** → results may not generalise to other makes/buses.
- The dataset's attacks are relatively coarse; subtle/stealthy injections are harder and under-tested.
- Near-perfect synthetic-data scores (like the prototype's) are a *wiring check*, not a result — report only real-dataset numbers.

## Tooling
`scikit-learn` (baseline + metrics), `torch` (CNN/LSTM), `matplotlib` (ROC + confusion plots).

## Definition of done
A re-runnable script that loads the dataset (or the synthetic generator), trains each model, and saves the metrics table + ROC/confusion plots. Committed and re-runnable (evidence rule); numbers refresh as the models improve.
