# Week 5 Protected Data Interface

**Owner:** Amit Das  
**Role:** Data Interface and Split Integrity Lead

## Week 5 Data Contract

The CNN receives the exact sequence arrays created from the corrected Week 3 pipeline:

```text
train sequences       → N × 64 × 11
validation sequences  → N × 64 × 11
test sequences        → N × 64 × 11
```

The authoritative class order is:

```text
Normal, DoS, Fuzzy, Gear, RPM
```

## Integrity Checks

- 64-frame windows.
- Stride 64.
- No shared-frame overlap.
- `source_class_chronological_v3`.
- All five classes in every split.
- No random resplitting in Week 5.
- No labels or attack ratio used as CNN input.
- Validation data used for checkpoint selection.
- Test data used only after model selection.

## Handover

Aahmad's recurrence encoder receives only the protected sequence arrays and integer class labels.
