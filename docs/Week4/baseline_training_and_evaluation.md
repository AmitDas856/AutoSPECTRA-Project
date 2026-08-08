# Week 4 Classical Baseline Training and Evaluation

**Owner:** Amit Das  
**Role:** Classical Baseline and Evaluation Lead

## Models

- Logistic Regression.
- Random Forest.
- Extra Trees.
- XGBoost when available.

All models use the same 24 engineered tabular features and the same protected Week 3 split.

## Evaluation

The shared harness reports:

- accuracy;
- balanced accuracy;
- macro precision;
- macro recall;
- macro-F1;
- weighted-F1;
- Matthews correlation coefficient;
- log loss;
- macro one-vs-rest ROC-AUC;
- macro PR-AUC;
- attack false-positive rate;
- attack false-negative rate;
- expected calibration error;
- inference milliseconds per window;
- throughput;
- saved model size;
- training time.

## Model-Selection Rule

Macro-F1 is the primary Week 4 comparison metric because it gives equal importance to all five classes.

## Important Boundary

Week 4 establishes tabular baselines only. Deep-learning models begin in Week 5.
