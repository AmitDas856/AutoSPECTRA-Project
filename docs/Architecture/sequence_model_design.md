# AutoSPECTRA LSTM and Autoencoder Design

## Purpose

The sequence branch models the temporal order of CAN identifiers, payload bytes and message timing. It contains:

1. a supervised LSTM classifier for five-class prediction; and
2. an autoencoder for anomaly detection.

These components have different purposes and must be evaluated separately.

## Sequence Representation

Each fixed-length window contains 64 ordered frames. A frame vector initially contains:

```text
normalized CAN ID
normalized DLC
eight normalized payload bytes
log-transformed inter-arrival time
```

Initial tensor shape:

```text
batch × 64 × 11
```

## CAN ID Representation

Week 1 preferred baseline:

- scale the numeric CAN ID to a bounded range.

Possible later comparison:

- learned CAN ID embedding.

The embedding option may improve representation but can also memorize vehicle-specific identifiers.

## Payload Representation

Each payload byte is converted from hexadecimal to an integer in the range 0–255 and scaled using training-set parameters.

Bytes beyond DLC are padded according to the documented parser policy. A mask or DLC feature must allow the model to distinguish real zero values from padding where necessary.

## Proposed LSTM Classifier

```text
Input sequence
→ LSTM layer
→ Dropout
→ optional second LSTM layer
→ final hidden representation
→ Dense layer
→ five-class output
→ Softmax
```

Initial settings to test:

- hidden size: 64 or 128;
- layers: 1 or 2;
- dropout: 0.2–0.4;
- weighted multiclass cross-entropy.

## LSTM Output Contract

The classifier returns an `N × 5` probability array in this order:

```text
Normal, DoS, Fuzzy, Gear, RPM
```

## Autoencoder Role

The autoencoder is an anomaly detector. It learns to reconstruct normal traffic windows.

Possible architecture:

```text
Input sequence
→ LSTM encoder
→ latent representation
→ repeated latent sequence
→ LSTM decoder
→ reconstructed sequence
```

## Reconstruction Error

A window-level anomaly score may be computed as mean squared reconstruction error across valid features and frames.

The score direction must be checked empirically:

```text
higher reconstruction error → more anomalous
```

No assumption should be made without validation.

## Anomaly Threshold

The anomaly threshold will be selected using validation data only.

Possible rule:

```text
threshold = percentile of validation normal reconstruction error
```

The selected percentile will be justified using false-positive rate and attack recall.

The test set must not be used to choose the threshold.

## Important Distinction

The autoencoder can indicate that a traffic window is anomalous. It does not automatically determine whether the attack is DoS, Fuzzy, Gear spoofing or RPM spoofing.

Attack-class attribution remains the responsibility of the supervised classifiers.

## Evaluation

For the LSTM classifier:

- accuracy;
- macro-F1;
- per-class recall;
- confusion matrix;
- ROC-AUC and PR-AUC;
- calibration;
- latency and model size.

For the autoencoder:

- binary normal-versus-attack ROC-AUC;
- PR-AUC;
- threshold-based recall;
- false-positive rate;
- reconstruction-error distribution;
- detection delay.

## Main Risks

- long training time;
- overfitting to CAN IDs;
- padded bytes may be confused with true zeros;
- a chronological split may omit a class unless splitting is source-aware;
- autoencoder scores may not transfer to another vehicle.

## Week 2 Tasks

- implement sequence tensor builder;
- confirm masking and padding strategy;
- implement small LSTM smoke test;
- train autoencoder on normal windows only;
- plot validation reconstruction-error distributions.
