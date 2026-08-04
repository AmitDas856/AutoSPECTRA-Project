# TinyCNN Results — CAN windows -> image -> CNN (WINDOW=32)

**Unit:** windows of 32 frames (window = attack if any injected frame inside). Frame-level baselines in results_week6.md are NOT directly comparable 1:1 — say so in the report.

- Train: 36,000 windows (capped stratified sample; 12000 Normal / 6000 per attack)
- Test: 155,337 windows = full held-out tail
- 3 epochs, batch 256, Adam 1e-3, CPU

## Per-class metrics

```
              precision    recall  f1-score   support

      Normal     0.9954    0.9854    0.9904    135612
         DoS     0.9515    0.9679    0.9596      1216
       Fuzzy     0.6498    0.8974    0.7538      3509
        Gear     0.8016    0.6513    0.7187      6860
         RPM     0.7488    0.8673    0.8037      8140

    accuracy                         0.9623    155337
   macro avg     0.8294    0.8739    0.8452    155337
weighted avg     0.9658    0.9623    0.9630    155337
```

**Macro-F1:** 0.8452 | **Macro ROC-AUC (ovr):** 0.9920

**FPR per class:** Normal 0.03138, DoS 0.00039, Fuzzy 0.01118, Gear 0.00745, RPM 0.01609

## Detection latency (window-level)

Latency = attack onset -> end of first correctly-flagged window, so the window length itself bounds the best case.

| Class | Episodes | Detected | Median ms | Max ms |
|---|---|---|---|---|
| DoS | 14 | 14 | 8.04 | 18.16 |
| Fuzzy | 25 | 25 | 0.00 | 107.45 |
| Gear | 37 | 37 | 11.44 | 25.54 |
| RPM | 40 | 40 | 11.04 | 77.32 |

Confusion matrix: `eval/confusion_TinyCNN_rec.png`

## Notes for the report

- Window labelling ('any injected frame') inflates attack support relative to frame counts; state the labelling rule explicitly.
- Trained on a capped subsample for CPU time; test coverage is full.
- Next ablation: WINDOW = 16 / 64, and recurrence-plot encoding vs the plain grid used here.
