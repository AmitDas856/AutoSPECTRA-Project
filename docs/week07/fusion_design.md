# Week 7 Fusion Design

**Owner:** Maheswari Kamireddy  
**Role:** Fusion, Ablation and Cross-Model Evaluation Lead

## Components

```text
Random Forest
Recurrence CNN
Bidirectional LSTM
```

## Weight Selection

Each component receives a raw weight equal to its validation macro-F1.

The weights are then normalised:

```text
weight_i = validation_macro_f1_i / sum(validation_macro_f1)
```

## Fusion

```text
fused_probability =
    RF_weight × RF_probability
  + CNN_weight × CNN_probability
  + LSTM_weight × LSTM_probability
```

Test labels are not used to determine the weights.

Fusion is retained as an architectural integration experiment even if it does not outperform the strongest standalone model.
