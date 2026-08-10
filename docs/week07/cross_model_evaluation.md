# Week 7 Cross-Model Evaluation

**Owner:** Maheswari Kamireddy

Week 7 compares:

- Logistic Regression;
- Random Forest;
- Extra Trees;
- XGBoost;
- Recurrence CNN;
- Bidirectional LSTM;
- uncalibrated RF + CNN + LSTM fusion;
- calibrated RF + CNN + LSTM fusion.

Main comparison dimensions:

- macro-F1;
- per-class F1;
- attack FPR/FNR;
- ROC-AUC and PR-AUC;
- expected calibration error;
- log loss;
- inference time;
- model/config size;
- estimated detection latency.

A more complex architecture is not automatically selected if a simpler model provides stronger or more reliable results.
