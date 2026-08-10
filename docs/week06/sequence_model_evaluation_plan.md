# Sequence Model Evaluation Plan

**Owner:** Maheswari Kamireddy

Bidirectional LSTM:
- macro-F1;
- per-class precision/recall/F1;
- ROC-AUC and PR-AUC;
- attack FPR/FNR;
- ECE and log loss;
- inference time and model size.

Autoencoder:
- binary precision, recall and F1;
- ROC-AUC and PR-AUC;
- FPR/FNR;
- anomaly-score distribution;
- threshold-search evidence.

The autoencoder is not a five-class classifier.
