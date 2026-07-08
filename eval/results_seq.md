# SeqLSTM Results — CAN window as a sequence -> LSTM (Week 7)

**Unit:** windows of 32 frames (window = attack if any injected frame inside). Same split and windowing as the CNN, so results_cnn.md is the direct comparison.

- Train: 36,000 windows (capped; 12000 Normal / 6000 per attack)
- Test: 155,337 windows = full held-out tail
- 3 epochs, batch 256, Adam 1e-3, CPU

## Per-class metrics

```
              precision    recall  f1-score   support

      Normal     0.9994    0.9991    0.9993    135612
         DoS     0.9648    0.9918    0.9781      1216
       Fuzzy     0.9737    0.9926    0.9831      3509
        Gear     0.9975    0.9964    0.9969      6860
         RPM     0.9994    0.9939    0.9966      8140

    accuracy                         0.9985    155337
   macro avg     0.9870    0.9947    0.9908    155337
weighted avg     0.9985    0.9985    0.9985    155337

```

**Macro-F1:** 0.9908 | **Macro ROC-AUC (ovr):** 0.9993

**FPR per class:** Normal 0.00385, DoS 0.00029, Fuzzy 0.00062, Gear 0.00011, RPM 0.00003

## Detection latency (window-level)

| Class | Episodes | Detected | Median ms | Max ms |
|---|---|---|---|---|
| DoS | 14 | 14 | 0.00 | 18.16 |
| Fuzzy | 25 | 25 | 0.00 | 88.21 |
| Gear | 37 | 37 | 0.00 | 14.83 |
| RPM | 40 | 40 | 0.00 | 22.70 |

Confusion matrix: `eval/confusion_SeqLSTM.png`
