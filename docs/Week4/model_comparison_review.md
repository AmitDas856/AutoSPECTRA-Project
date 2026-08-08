# Week 4 Classical Model Comparison Review

**Owner:** Maheswari Kamireddy  
**Role:** Model Comparison Lead

## Models Compared

1. Logistic Regression.
2. Random Forest.
3. Extra Trees.
4. XGBoost.

## Comparison Dimensions

- macro-F1;
- per-class precision;
- per-class recall;
- per-class F1;
- attack false-positive rate;
- attack false-negative rate;
- ROC-AUC;
- PR-AUC;
- expected calibration error;
- training time;
- inference time per window;
- throughput;
- saved model size.

## Review Questions

- Does the highest-accuracy model also have the highest macro-F1?
- Which model has the smallest attack FNR?
- Does any model produce false alarms on Normal traffic?
- Does a small increase in macro-F1 require substantially more computation?
- Are Gear and RPM spoofing equally well separated?
- Is the simpler model competitive enough to remain a deployment fallback?

## Week Boundary

This comparison establishes the tabular baseline against which Week 5 CNN and Week 6 LSTM results will later be assessed.
