# Week 3 Technical Meeting Notes

**Date:**  
**Chair:** Miftha Thahniyath  
**Attendees:** Amit Das, Aahmad Sayeed, Maheswari Kamireddy, Miftha Thahniyath, Nagireddy Nakka

## Topics

1. Window size and stride.
2. Window-label rule.
3. Source/class reservoir sampling.
4. Chronological train/validation/test boundaries.
5. Test-set protection.
6. Tabular, sequence and recurrence representations.
7. Metadata and data lineage.
8. Week 4 baseline handover.

## Decisions

| Decision | Reason |
|---|---|
| Use 64-frame windows | Fixed input for tabular, CNN and LSTM branches |
| Use stride 64 | Prevent shared-frame overlap |
| Use source/class chronological partitions | Preserve class coverage while reducing temporal leakage |
| Retain global row position | Enables chronology and overlap audits |
| Keep attack ratio as metadata only | Prevent direct target leakage |
| Do not train models in Week 3 | Maintain incremental GitHub evidence |

## Actions

| Member | Action |
|---|---|
| Amit | Finalise windowing, split and notebook |
| Aahmad | Validate recurrence transformation |
| Maheswari | Validate sequence tensor |
| Miftha | Document metadata and meeting |
| Nagireddy | Review leakage, ethics and reproducibility |
