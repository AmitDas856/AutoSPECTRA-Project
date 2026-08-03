# AutoSPECTRA System Architecture — Week 1 Baseline

This diagram records the architecture agreed during Week 1. It is expected to evolve through reviewed pull requests.

```mermaid
flowchart LR
    A1[HCRL Car-Hacking Dataset] --> B
    A2[Synthetic CAN Generator] --> B
    A3[Uploaded CAN Log for Demo] --> B

    subgraph DP[Data Pipeline]
        B[CAN Frame Parser]
        C[Schema and Range Validation]
        D[Hexadecimal to Numeric Conversion]
        E[Source-Aware Chronological Split]
        F[Sliding Window Builder]
        G[Feature Engineering]
        B --> C --> D --> E --> F --> G
    end

    G --> H1
    G --> H2
    F --> H3
    F --> H4

    subgraph AI[AI Detection Layer]
        H1[Random Forest / XGBoost Baseline]
        H2[Tabular Features]
        H3[Recurrence-Style Image Encoder]
        H4[CAN ID and Payload Sequences]
        H3 --> I1[CNN Classifier]
        H4 --> I2[LSTM Classifier]
        H4 --> I3[Autoencoder Anomaly Detector]
        H2 --> H1
    end

    H1 --> J
    I1 --> J
    I2 --> J
    I3 --> J

    J[Probability Fusion and Calibration] --> K[Five-Class Prediction]
    K --> L1[Attack Type]
    K --> L2[Confidence]
    K --> L3[Detection Latency]

    subgraph OUT[Explanation and Delivery]
        L1 --> M[Rule-Based Incident Report Generator]
        L2 --> M
        L3 --> M
        M --> N[Flask Dashboard and Live Demo]
        M --> O[Structured JSON / CSV Report]
    end

    subgraph EVAL[Evaluation and Governance]
        P[Evaluation Harness]
        Q[Accuracy, Macro-F1, Per-Class Recall]
        R[Confusion Matrix, ROC-AUC, PR-AUC]
        S[False Alarms, Detection Delay, Model Size]
        T[Ethics, Privacy, Dual Use, Human Oversight]
        P --> Q
        P --> R
        P --> S
        P --> T
    end

    H1 --> P
    I1 --> P
    I2 --> P
    I3 --> P
    J --> P
```

## Architectural decisions recorded in Week 1

1. **The split must be source-aware and chronological.** Randomly mixing nearby CAN frames across training and testing can inflate results.
2. **A conventional baseline is mandatory.** Random Forest or XGBoost provides a transparent and dependable comparison.
3. **CNN and LSTM branches answer different questions.** The CNN learns image-encoded traffic patterns; the LSTM learns temporal dependencies.
4. **The autoencoder is an anomaly detector, not automatically a five-class classifier.**
5. **Fusion must be validated.** The combined model is retained only if it improves macro-F1, attack recall or calibration without unacceptable latency.
6. **The report generator is symbolic and controlled.** It converts structured detection evidence into a human-readable report.
7. **No automated vehicle control.** The prototype generates decision-support alerts only.
