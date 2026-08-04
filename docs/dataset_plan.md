# Dataset Acquisition and Handling Plan

## Proposed main dataset

HCRL Car-Hacking dataset, distributed through a public research source and a Kaggle mirror.

Expected files:

- `DoS_dataset.csv`
- `Fuzzy_dataset.csv`
- `gear_dataset.csv`
- `RPM_dataset.csv`
- `normal_run_data.txt` where available

## Data handling

- Do not commit dataset files to GitHub.
- Keep original files read-only.
- Record file names, sizes and checksums.
- Preserve source-capture identity.
- Parse variable-length payloads according to DLC.
- Convert hexadecimal values only after validation.
- Create train, validation and test ranges inside each source capture.
- Fit scalers, encoders and thresholds on training/validation data only.
- Report class support in every split.

## Week 1 deliverable

Create `data/dataset_manifest.example.csv`, then produce a local private copy containing actual checksums after download.
