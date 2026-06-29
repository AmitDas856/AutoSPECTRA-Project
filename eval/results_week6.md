# Baseline Results — Week 6

**Model:** Decision Tree (max_depth=20, trained on 20% sample of train set)
**Split:** Per-file time-ordered 70/30 — no leakage

- Train frames: 11,598,631 (used 2,319,726 = 20%)
- Test frames:  4,970,844

## Per-class Precision / Recall / F1

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

## False-Positive Rate per class

| Class | FPR |
|---|---|
| Normal | 0.0001 |
| DoS | 0.0000 |
| Fuzzy | 0.0000 |
| Gear | 0.0000 |
| RPM | 0.0000 |

## ROC-AUC

Macro ROC-AUC (one-vs-rest): **0.9999**

## Critical analysis (for Report Part D)

Scores are very high because:
1. The HCRL attacks are coarse injections on a *single* 2010 Hyundai Sonata.
   Injected frames differ obviously in payload patterns from normal traffic,
   making them easy for even a shallow tree to separate.
2. DoS floods at fixed IDs; Fuzzy randomises all bytes — both create strong
   statistical signatures a Decision Tree exploits trivially.
3. These scores do NOT mean the system would work on a different vehicle,
   a different CAN bus speed, or against a subtle stealthy attacker who
   mimics normal traffic patterns.

The *evaluation* contribution is: honest split + per-class FPR + latency,
not the headline number. A false alarm in a moving car is dangerous;
the FPR column is the number that matters for safety.
[VERIFY — write this in your own words for Part D]
