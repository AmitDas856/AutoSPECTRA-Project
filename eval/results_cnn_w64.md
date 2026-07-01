# TinyCNN Results — CAN windows -> image -> CNN (WINDOW=64)

**Unit:** windows of 64 frames (window = attack if any injected frame inside). Frame-level baselines in results_week6.md are NOT directly comparable 1:1 — say so in the report.

- Train: 36,000 windows (capped stratified sample; 12000 Normal / 6000 per attack)
- Test: 77,668 windows = full held-out tail
- 3 epochs, batch 256, Adam 1e-3, CPU

## Per-class metrics

```
              precision    recall  f1-score   support

      Normal     0.9992    0.9999    0.9995     67748
         DoS     0.9854    0.9918    0.9886       613
       Fuzzy     0.9994    0.9898    0.9946      1768
        Gear     1.0000    0.9942    0.9971      3451
         RPM     0.9990    0.9971    0.9980      4088

    accuracy                         0.9992     77668
   macro avg     0.9966    0.9946    0.9956     77668
weighted avg     0.9992    0.9992    0.9992     77668
```

**Macro-F1:** 0.9956 | **Macro ROC-AUC (ovr):** 0.9994

**FPR per class:** Normal 0.00514, DoS 0.00012, Fuzzy 0.00001, Gear 0.00000, RPM 0.00005

## Detection latency (window-level)

Latency = attack onset -> end of first correctly-flagged window, so the window length itself bounds the best case.

| Class | Episodes | Detected | Median ms | Max ms |
|---|---|---|---|---|
| DoS | 14 | 14 | 0.00 | 16.47 |
| Fuzzy | 25 | 25 | 0.00 | 255.61 |
| Gear | 37 | 37 | 0.00 | 24.52 |
| RPM | 40 | 40 | 0.00 | 30.34 |

Confusion matrix: `eval/confusion_TinyCNN_w64.png`

## Notes for the report

- Window labelling ('any injected frame') inflates attack support relative to frame counts; state the labelling rule explicitly.
- Trained on a capped subsample for CPU time; test coverage is full.
- Next ablation: WINDOW = 16 / 64, and recurrence-plot encoding vs the plain grid used here.
