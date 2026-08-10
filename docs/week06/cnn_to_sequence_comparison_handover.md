# CNN-to-Sequence Comparison Handover

**Owner:** Aahmad Sayeed

Week 5 CNN and Week 6 LSTM share the same:
- windows;
- class order;
- train/validation/test split;
- held-out test windows;
- validation-based checkpoint selection;
- class-aware metrics.

Representation difference:

```text
CNN  → 64 × 64 recurrence image
LSTM → 64 × 11 chronological sequence
```

This preserves a fair Week 7 CNN-versus-LSTM comparison.
