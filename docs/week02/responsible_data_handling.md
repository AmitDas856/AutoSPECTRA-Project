# Week 2 Responsible Data Handling

**Owner:** Nagireddy Nakka  
**Role:** Ethics and Documentation Lead

## Repository Controls

Do not commit:

```text
DoS_dataset.csv
Fuzzy_dataset.csv
gear_dataset.csv
RPM_dataset.csv
normal_run_data.txt
*.npz
*.joblib
*.pt
*.pth
*.pkl
*.zip
.env
API tokens
```

## Defensive-Use Position

AutoSPECTRA is an academic defensive monitoring prototype. Week 2 code reads and audits public research captures. It does not inject traffic, modify a vehicle or control a safety-critical function.

## Human Oversight

Later alerts must remain decision support. They must not automatically control braking, steering, engine, transmission or other vehicle systems.
