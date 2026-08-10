# Week 6 Critical Evaluation and Responsible AI

**Owner:** Nagireddy Nakka

Key risks:
- missed attacks;
- high-confidence wrong LSTM predictions;
- spoofing-class confusion;
- dataset-specific CAN-ID shortcuts;
- autoencoder threshold sensitivity;
- autoencoder attacks that reconstruct like Normal traffic;
- strong precision with insufficient recall.

The autoencoder threshold and score direction must come from validation data only. Neither sequence model is a certified automotive IDS or autonomous controller.
