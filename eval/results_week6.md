# Baseline Results — Week 6 (tabular models)

**Split:** per-file time-ordered 70/30, leakage assert passes per file.
**Train:** 11,598,631 frames (models fit on 20% stratified sample = 2,319,726). **Test:** 4,970,844 frames (full held-out tail, all 5 classes).

## Model comparison (frame-level, full test set)

| Model | Macro-F1 | ROC-AUC (ovr) | Worst-class FPR |
|---|---|---|---|
| DecisionTree | 0.9999 | 0.9999 | 0.00012 |
| RandomForest | 1.0000 | 1.0000 | 0.00000 |

## DecisionTree

```
              precision    recall  f1-score   support

      Normal     1.0000    1.0000    1.0000   4754568
         DoS     1.0000    1.0000    1.0000     21164
       Fuzzy     0.9999    0.9994    0.9996     43423
        Gear     1.0000    1.0000    1.0000     69037
         RPM     1.0000    1.0000    1.0000     82652

    accuracy                         1.0000   4970844
   macro avg     1.0000    0.9999    0.9999   4970844
weighted avg     1.0000    1.0000    1.0000   4970844
```

**False-positive rate per class:** Normal 0.00012, DoS 0.00000, Fuzzy 0.00000, Gear 0.00000, RPM 0.00000

**Detection latency** (episode = burst of attack frames with <1s gaps; latency = attack onset → first correctly-flagged frame):

| Class | Episodes | Detected | Median ms | Max ms | Median frames |
|---|---|---|---|---|---|
| DoS | 14 | 14 | 0.00 | 0.00 | 0 |
| Fuzzy | 25 | 25 | 0.00 | 0.00 | 0 |
| Gear | 37 | 37 | 0.00 | 0.00 | 0 |
| RPM | 40 | 40 | 0.00 | 0.00 | 0 |

Confusion matrix: `eval/confusion_DecisionTree.png`

## RandomForest

```
              precision    recall  f1-score   support

      Normal     1.0000    1.0000    1.0000   4754568
         DoS     1.0000    1.0000    1.0000     21164
       Fuzzy     1.0000    1.0000    1.0000     43423
        Gear     1.0000    1.0000    1.0000     69037
         RPM     1.0000    1.0000    1.0000     82652

    accuracy                         1.0000   4970844
   macro avg     1.0000    1.0000    1.0000   4970844
weighted avg     1.0000    1.0000    1.0000   4970844
```

**False-positive rate per class:** Normal 0.00000, DoS 0.00000, Fuzzy 0.00000, Gear 0.00000, RPM 0.00000

**Detection latency** (episode = burst of attack frames with <1s gaps; latency = attack onset → first correctly-flagged frame):

| Class | Episodes | Detected | Median ms | Max ms | Median frames |
|---|---|---|---|---|---|
| DoS | 14 | 14 | 0.00 | 0.00 | 0 |
| Fuzzy | 25 | 25 | 0.00 | 0.00 | 0 |
| Gear | 37 | 37 | 0.00 | 0.00 | 0 |
| RPM | 40 | 40 | 0.00 | 0.00 | 0 |

Confusion matrix: `eval/confusion_RandomForest.png`

## Critical analysis (notes for Report Part D — write in own words)

- Near-perfect scores are EXPECTED on this dataset, not impressive: the
  HCRL attacks are coarse injections on a single 2010 Hyundai Sonata.
  DoS floods a fixed CAN ID (0x000) and Fuzzy randomises whole payloads —
  both leave signatures a shallow tree separates trivially.
- The comparison DT vs RF therefore shows near-identical headline numbers;
  the informative columns are FPR (false alarms erode driver trust) and
  detection latency (an IDS that flags after the crash is useless).
- Latency here is measured per attack EPISODE, strict correct-class flag.
- These results say nothing about a different vehicle, bus load, or a
  stealthy attacker that mimics normal traffic. Single-vehicle bias is
  the headline limitation for Part D.
