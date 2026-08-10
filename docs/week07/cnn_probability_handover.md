# Week 7 CNN Probability Handover

**Owner:** Aahmad Sayeed  
**Role:** CNN Evidence and Calibration Visualisation Reviewer

The Week 5 Recurrence CNN contributes validation and test probability matrices to the Week 7 fusion layer.

## Required Interface

```text
validation probabilities → validation windows × 5 classes
test probabilities       → test windows × 5 classes
```

The row order must remain identical to the protected sequence/test metadata order.

## Checks

- class order remains Normal, DoS, Fuzzy, Gear, RPM;
- every probability row sums approximately to 1;
- no label or attack ratio is used as input;
- validation probabilities determine the CNN's fusion weight;
- test probabilities never determine fusion weight.
