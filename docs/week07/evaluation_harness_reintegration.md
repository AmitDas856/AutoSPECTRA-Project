# Week 7 Evaluation Harness Reintegration

**Owner:** Amit Das  
**Role:** Evaluation Harness and Fusion Integration Lead

## Purpose

Week 7 reuses one evaluation harness for the classical and deep-learning models so that every multiclass result is calculated under the same protocol.

## Reintegrated Model Outputs

- Random Forest validation/test probabilities.
- Recurrence CNN validation/test probabilities.
- Bidirectional LSTM validation/test probabilities.
- saved prediction arrays;
- per-model inference time;
- model size;
- class-aware evaluation metrics.

## Shared Metrics

- accuracy;
- balanced accuracy;
- macro precision;
- macro recall;
- macro-F1;
- weighted-F1;
- MCC;
- one-vs-rest ROC-AUC;
- macro PR-AUC;
- attack FPR;
- attack FNR;
- expected calibration error;
- log loss;
- inference milliseconds per window;
- throughput;
- model size.

## Test Isolation

Validation data selects fusion weights and calibration temperature. Test labels are used only for final evaluation.
