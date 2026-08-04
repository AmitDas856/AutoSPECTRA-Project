# Week 2 Data Pipeline Implementation

**Owner:** Amit Das  
**Role:** Data Pipeline and Integration Lead

## Work Completed

- Located the four required HCRL source captures inside Kaggle.
- Implemented chunk-based processing for multi-million-row files.
- Implemented a DLC-aware parser because the final `R` or `T` flag changes position according to DLC.
- Converted timestamps to numeric values.
- Converted hexadecimal CAN IDs to integers.
- Converted available payload bytes to numeric values.
- Padded unavailable payload positions only for a consistent audit table.
- Retained source capture and normal/attack flag information.
- Exported small CSV and JSON audit evidence.

## Source Files

```text
DoS_dataset.csv
Fuzzy_dataset.csv
gear_dataset.csv
RPM_dataset.csv
```

## Important Boundary

This Week 2 pipeline audits raw captures only. The final 64-frame windows, chronological split and model-ready representations are reserved for Week 3.
