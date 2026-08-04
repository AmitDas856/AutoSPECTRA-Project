# TinyCNN Results — CAN windows -> image -> CNN (WINDOW=16)

**Unit:** windows of 16 frames (window = attack if any injected frame inside). Frame-level baselines in results_week6.md are NOT directly comparable 1:1 — say so in the report.

- Train: 36,000 windows (capped stratified sample; 12000 Normal / 6000 per attack)
- Test: 310,675 windows = full held-out tail
- 3 epochs, batch 256, Adam 1e-3, CPU

## Per-class metrics

```
              precision    recall  f1-score   support

      Normal     0.9973    0.9927    0.9950    271353
         DoS     1.0000    0.9661    0.9828      2419
       Fuzzy     0.7374    0.9649    0.8359      6978
        Gear     0.9885    0.9651    0.9766     13678
         RPM     0.9916    0.9616    0.9764     16247

    accuracy                         0.9890    310675
   macro avg     0.9430    0.9701    0.9533    310675
weighted avg     0.9908    0.9890    0.9895    310675
```

**Macro-F1:** 0.9533 | **Macro ROC-AUC (ovr):** 0.9978

**FPR per class:** Normal 0.01849, DoS 0.00000, Fuzzy 0.00790, Gear 0.00052, RPM 0.00045

## Detection latency (window-level)

Latency = attack onset -> end of first correctly-flagged window, so the window length itself bounds the best case.

| Class | Episodes | Detected | Median ms | Max ms |
|---|---|---|---|---|
| DoS | 14 | 14 | 3.97 | 8.79 |
| Fuzzy | 25 | 25 | 0.00 | 6.26 |
| Gear | 37 | 37 | 0.00 | 11.92 |
| RPM | 40 | 40 | 0.00 | 14.29 |

Confusion matrix: `eval/confusion_TinyCNN_w16.png`

## Notes for the report

- Window labelling ('any injected frame') inflates attack support relative to frame counts; state the labelling rule explicitly.
- Trained on a capped subsample for CPU time; test coverage is full.
- Next ablation: WINDOW = 16 / 64, and recurrence-plot encoding vs the plain grid used here.
