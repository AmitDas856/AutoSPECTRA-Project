# Protected Sequence Interface

**Owner:** Amit Das

The Week 6 models use the exact protected sequence arrays produced by the Week 3 pipeline.

```text
Train      → N × 64 × 11
Validation → N × 64 × 11
Test       → N × 64 × 11
```

Checks:
- 64-frame windows;
- stride 64;
- `source_class_chronological_v3`;
- no random resplit;
- class order remains Normal, DoS, Fuzzy, Gear, RPM;
- sequence, label and metadata rows remain aligned;
- test data is not used for checkpoint or threshold selection.
