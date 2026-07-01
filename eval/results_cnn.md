# TinyCNN Results — CAN windows -> image -> CNN (Week 6)

**Unit:** windows of 32 frames (window = attack if any injected frame inside). Frame-level baselines in results_week6.md are NOT directly comparable 1:1 — say so in the report.

- Train: 36,000 windows (capped stratified sample; 12000 Normal / 6000 per attack)
- Test: 155,337 windows = full held-out tail
- 3 epochs, batch 256, Adam 1e-3, CPU

## Per-class metrics

```
              precision    recall  f1-score   support

      Normal     0.9994    0.9972    0.9983    135612
         DoS     1.0000    0.9827    0.9913      1216
       Fuzzy     0.9010    0.9937    0.9451      3509
        Gear     0.9994    0.9949    0.9972      6860
         RPM     0.9970    0.9959    0.9965      8140

    accuracy                         0.9969    155337
   macro avg     0.9794    0.9929    0.9857    155337
weighted avg     0.9971    0.9969    0.9969    155337
```

**Macro-F1:** 0.9857 | **Macro ROC-AUC (ovr):** 0.9993

**FPR per class:** Normal 0.00380, DoS 0.00000, Fuzzy 0.00252, Gear 0.00003, RPM 0.00016

## Detection latency (window-level)

Latency = attack onset -> end of first correctly-flagged window, so the window length itself bounds the best case.

| Class | Episodes | Detected | Median ms | Max ms |
|---|---|---|---|---|
| DoS | 14 | 14 | 0.00 | 18.16 |
| Fuzzy | 25 | 25 | 0.00 | 88.21 |
| Gear | 37 | 37 | 0.00 | 14.83 |
| RPM | 40 | 40 | 0.00 | 22.70 |

Confusion matrix: `eval/confusion_TinyCNN.png`

## Notes for the report

- Window labelling ('any injected frame') inflates attack support relative to frame counts; state the labelling rule explicitly.
- Trained on a capped subsample for CPU time; test coverage is full.
- Next ablation: WINDOW = 16 / 64, and recurrence-plot encoding vs the plain grid used here.
