# LSTM Autoencoder Design and Thresholding

**Owner:** Maheswari Kamireddy

The autoencoder is trained only on Normal windows from the training split.

```text
64 × 11
→ LSTM encoder, hidden 48
→ repeated context
→ LSTM decoder, hidden 48
→ reconstruct 11 channels
```

Anomaly score = mean squared reconstruction error.

Threshold governance:
- evaluate both higher-error-is-attack and lower-error-is-attack;
- generate candidate thresholds from validation quantiles;
- prefer highest validation F1 subject to validation FPR ≤ 0.10;
- never use the test set to choose direction or threshold.
