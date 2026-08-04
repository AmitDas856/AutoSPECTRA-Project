# AutoSPECTRA

## Deep-Learning Intrusion Detection and Incident Reporting for Connected-Car CAN Bus Traffic

<p align="center">
  <img
    src="docs/images/autospectra_architecture.png"
    alt="AutoSPECTRA system architecture"
    width="100%"
  />
</p>


<p align="center">
  <strong>Five-class CAN-bus intrusion detection using machine learning, computer vision, sequence modelling, anomaly detection, calibrated fusion and controlled incident reporting.</strong>
</p>

---

## Project Overview

**AutoSPECTRA** is an academic defensive cybersecurity prototype that analyses Controller Area Network (CAN) traffic from connected vehicles and classifies each traffic window into one of five classes:

- **Normal**
- **DoS**
- **Fuzzy**
- **Gear spoofing**
- **RPM spoofing**

The project combines several artificial-intelligence approaches:

- engineered-feature machine learning;
- recurrence-image computer vision;
- sequential deep learning;
- unsupervised anomaly detection;
- weighted probability fusion;
- confidence calibration;
- rule-based natural-language incident reporting;
- Flask-based demonstration and deployment.

AutoSPECTRA is designed as a **decision-support and research system**. It is not certified for real-vehicle deployment and must not automatically control braking, steering, engine, transmission or other safety-critical vehicle functions.

---

## Module Information

| Field | Details |
|---|---|
| Module | Advanced Artificial Intelligence Projects in Data Science |
| Module code | 55-710603 |
| Assessment | AI Project and Pitch |
| Group | Group 7 |
| Project | AutoSPECTRA |
| Main dataset | HCRL Car-Hacking Dataset |
| Development environment | Kaggle, Python, scikit-learn, XGBoost, PyTorch and Flask |

---

## Team

| Member | Name | Main Role |
|---|---|---|
| 1 | Amit Das | Data Pipeline, Evaluation and Repository Integration Lead |
| 2 | Aahmad Sayeed | EDA, Recurrence Representation and CNN Lead |
| 3 | Maheswari Kamireddy | LSTM and Autoencoder Sequence-Modelling Lead |
| 4 | Miftha Thahniyath | Incident Reporting, Flask and Demonstration Lead |
| 5 | Nagireddy Nakka | Ethics, Responsible AI and Documentation Lead |

All members are expected to maintain individual GitHub evidence through branches, issues, pull requests, reviews and descriptive commits.

---

## Research Aim

The project aims to design and critically evaluate a reproducible AI workflow for connected-car CAN-bus intrusion detection while addressing:

- class imbalance;
- temporal and source leakage;
- class-coverage problems;
- false alarms and missed attacks;
- opaque predictions;
- probability calibration;
- computational cost;
- responsible-AI requirements;
- human oversight;
- limitations of one-vehicle benchmark data.

---

## System Architecture

The complete workflow is:

```text
HCRL CAN-bus captures
        ↓
Dataset discovery and file validation
        ↓
Memory-efficient DLC-aware parser
        ↓
Chronological 64-frame windows
        ↓
Source-aware and class-aware split
        ↓
 ┌─────────────────────────────────────────────────────────────┐
 │ 24 engineered tabular features                             │
 │ 64 × 11 sequential representation                          │
 │ 64 × 64 recurrence-style image representation              │
 └─────────────────────────────────────────────────────────────┘
        ↓
 ┌─────────────────────────────────────────────────────────────┐
 │ Logistic Regression                                        │
 │ Random Forest                                              │
 │ Extra Trees                                                │
 │ XGBoost                                                    │
 │ Recurrence CNN                                             │
 │ Bidirectional LSTM                                         │
 │ Normal-only LSTM Autoencoder                               │
 └─────────────────────────────────────────────────────────────┘
        ↓
Weighted RF + CNN + LSTM probability fusion
        ↓
Temperature calibration
        ↓
Five-class prediction
        ↓
Structured JSON and plain-language incident report
        ↓
Flask demonstration application
```

---

## Dataset

The project uses four HCRL attack-capture files:

```text
DoS_dataset.csv
Fuzzy_dataset.csv
gear_dataset.csv
RPM_dataset.csv
```

The notebook discovers these files recursively inside the Kaggle input directory.

The independent `normal_run_data.txt` file may also be detected, but the main five-class experiment derives Normal windows from legitimate `R` frames inside the four attack captures.

### Important dataset limitation

The benchmark represents one vehicle environment. Strong within-dataset performance does not establish cross-vehicle or real-road generalisation.

Raw dataset files are not stored in this repository.

---

## Data Pipeline

### DLC-aware parsing

The raw dataset contains variable-length payloads. The final `R` or `T` flag therefore does not always appear in a fixed CSV column.

The parser:

1. reads timestamps, CAN IDs and DLC;
2. uses DLC to identify valid payload positions;
3. locates the final normal/attack flag;
4. converts hexadecimal CAN IDs and payload bytes;
5. pads unavailable payload positions to a consistent eight-byte format;
6. processes the large source files in chunks;
7. records invalid or dropped rows;
8. preserves the original chronological order.

### Windowing

The primary experiment uses:

| Setting | Value |
|---|---:|
| Window size | 64 CAN frames |
| Stride | 64 CAN frames |
| Overlap | None |
| Minimum injected frames | 1 |
| Classes | 5 |

A window is labelled:

- **Normal** when it contains no injected `T` frame;
- as its source attack class when it contains at least one injected frame.

The attack-frame ratio is retained as audit metadata and is not used as a model feature.

### Split strategy

The corrected split is described as:

> Source-aware, class-aware, chronologically partitioned reservoir sampling.

The sampled windows remain associated with their source and class, are sorted by original source position and are divided chronologically into:

```text
70% training
15% validation
15% testing
```

The implementation explicitly checks that all five classes are represented in every split.

---

## Feature Representations

### Tabular features

Each 64-frame window is converted into 24 engineered features covering:

- message duration and rate;
- inter-arrival-time statistics;
- CAN-ID diversity and entropy;
- dominant-ID behaviour;
- CAN-ID transitions;
- DLC statistics;
- payload mean, standard deviation and entropy;
- non-zero-byte ratio;
- payload-byte change;
- payload-sum statistics.

### Sequential representation

Each window becomes a:

```text
64 × 11
```

sequence containing:

- normalised CAN ID;
- normalised DLC;
- eight normalised payload bytes;
- log-scaled inter-arrival time.

### Recurrence-image representation

Each sequence is compressed into a one-dimensional signal and converted into a:

```text
64 × 64
```

pairwise recurrence-style image used by the CNN.

---

## Models

### Classical machine learning

- Logistic Regression
- Random Forest
- Extra Trees
- XGBoost

### Deep learning

- Recurrence-image CNN
- Bidirectional LSTM classifier
- LSTM autoencoder

### Fusion

Validation macro-F1 is used to derive component weights for:

- Random Forest;
- recurrence CNN;
- LSTM classifier.

The weighted probabilities are then calibrated using temperature scaling.

---

## Evaluation

The project evaluates:

- accuracy;
- balanced accuracy;
- per-class precision;
- per-class recall;
- per-class F1;
- macro-F1;
- weighted-F1;
- confusion matrices;
- one-vs-rest ROC-AUC;
- one-vs-rest PR-AUC;
- false-positive rate;
- false-negative rate;
- model size;
- inference time;
- estimated detection latency;
- calibration error;
- feature ablations;
- model-fusion behaviour;
- reconstruction-error anomaly detection.

The main model-selection measure is **macro-F1** because all five classes must contribute equally to the evaluation.

---

## Main Results

The stored final run used balanced fast-mode samples:

| Split | Windows | Per class |
|---|---:|---:|
| Training | 17,500 | 3,500 |
| Validation | 4,000 | 800 |
| Test | 4,000 | 800 |

### Multiclass comparison

| Model | Accuracy | Macro-F1 |
|---|---:|---:|
| Random Forest | 0.99775 | 0.997754 |
| XGBoost | 0.99775 | 0.997754 |
| Extra Trees | 0.99725 | 0.997256 |
| Logistic Regression | 0.99650 | 0.996511 |
| Calibrated fusion | 0.99525 | 0.995270 |
| Bidirectional LSTM | 0.99475 | 0.994771 |
| Recurrence CNN | 0.98050 | 0.980563 |

Random Forest and XGBoost achieved the joint-highest test macro-F1.

Random Forest is retained as the principal deployment baseline because it is:

- highly accurate;
- computationally efficient;
- easier to interpret;
- suitable as a reliable Flask fallback.

### Autoencoder

The normal-only LSTM autoencoder achieved:

| Metric | Result |
|---|---:|
| Accuracy | 0.6895 |
| Precision | 0.9558 |
| Recall | 0.6416 |
| F1 | 0.7678 |
| ROC-AUC | 0.7135 |
| PR-AUC | 0.9322 |

The autoencoder is therefore treated as a secondary anomaly signal rather than the primary detector.

### Calibration

Temperature scaling reduced the fusion model's expected calibration error from approximately:

```text
0.024620 → 0.001828
```

Calibration improved confidence quality but did not change the predicted classes.

---

## Feature-Ablation Findings

| Feature group | Macro-F1 |
|---|---:|
| CAN ID and timing | 0.997754 |
| All 24 features | 0.997505 |
| CAN ID only | 0.997505 |
| Payload only | 0.993527 |
| Timing only | 0.707266 |

These findings suggest that CAN identifiers carry much of the predictive signal in this benchmark.

This is also a limitation: the models may learn vehicle- or capture-specific identifier patterns rather than universally transferable attack behaviour.

---

## Estimated Detection Latency

The notebook estimates latency from the first injected frame in a correctly classified window to the end of that window.

Approximate median upper-bound latency:

| Attack | Median latency |
|---|---:|
| RPM spoofing | 25.75 ms |
| Gear spoofing | 28.92 ms |
| Fuzzy | Approximately 53–54 ms |
| DoS | Approximately 55–56 ms |

These values are window-completion estimates, not complete in-vehicle response times.

---

## Incident Reporting

The reporting component produces controlled and reproducible outputs rather than unrestricted generative text.

Each report can contain:

- selected model;
- predicted class;
- confidence;
- severity;
- window start and end timestamps;
- window size;
- dominant CAN ID;
- message rate;
- unique CAN-ID count;
- CAN-ID entropy;
- recommended defensive action;
- human-oversight warning.

Example output structure:

```json
{
  "system": "AutoSPECTRA",
  "predicted_class": "DoS",
  "confidence": 0.97,
  "severity": "High",
  "window_size_frames": 64,
  "dominant_can_id": "0x000",
  "recommended_action": "Alert the operator and inspect the affected CAN segment.",
  "human_oversight": "Decision-support alert only. Do not automatically control safety-critical vehicle functions."
}
```

---

## Flask Application

The final notebook exports a Flask deployment package containing:

- trained model files;
- preprocessing functions;
- model-fusion configuration;
- calibration parameters;
- incident-report generator;
- HTML templates;
- CSS and static assets;
- upload and prediction routes;
- CSV and JSON downloads;
- local run scripts.

The main demonstration flow is:

```text
Upload unseen CAN log
        ↓
Validate and parse
        ↓
Create chronological windows
        ↓
Generate model probabilities
        ↓
Display prediction and confidence
        ↓
Generate incident report
        ↓
Download structured results
```

---

## Eight-Week Development Plan

| Week | Main GitHub Evidence |
|---|---|
| Week 1 | Repository setup, project charter, architecture, roles and ethics baseline |
| Week 2 | Dataset acquisition, DLC-aware parsing, source audit and initial EDA |
| Week 3 | Windowing, chronological split, leakage tests and feature representations |
| Week 4 | Classical machine-learning baselines |
| Week 5 | Recurrence-image encoder and CNN |
| Week 6 | Bidirectional LSTM and LSTM autoencoder |
| Week 7 | Fusion, calibration, ablation, latency, error analysis and responsible AI |
| Week 8 | Incident reports, Flask application, live demonstration and final package |

---

## Repository Structure

```text
AutoSPECTRA-CAN-IDS/
├── README.md
├── requirements.txt
├── .gitignore
├── configs/
│   ├── week1_baseline.yaml
│   ├── week02_audit.yaml
│   └── week2_experiment.yaml
├── data/
│   ├── README.md
│   └── dataset_manifest.example.csv
├── docs/
│   ├── images/
│   │   └── autospectra_architecture.png
│   ├── architecture/
│   ├── ethics/
│   ├── literature/
│   ├── meeting-notes/
│   ├── project-management/
│   ├── testing/
│   └── week02/
├── notebooks/
│   ├── week02/
│   │   └── autospectra_week02_dataset_audit_eda.ipynb
│   └── autospectra_end_to_end.ipynb
├── results/
│   └── week02/
├── scripts/
│   ├── check_project_structure.py
│   └── validate_week02_notebook.py
├── src/
│   └── autospectra/
└── tests/
    ├── test_repository_scaffold.py
    └── test_week02_notebook_structure.py
```

---

## Running the Week 2 Notebook

1. Open Kaggle.
2. Create a new notebook.
3. Attach the HCRL Car-Hacking dataset.
4. Upload:

```text
notebooks/week02/autospectra_week02_dataset_audit_eda.ipynb
```

5. Run all cells from top to bottom.

The Week 2 notebook generates:

```text
/kaggle/working/AutoSPECTRA_Week02_Evidence.zip
```

The ZIP contains small audit tables, JSON summaries and EDA figures. It does not contain the raw dataset.

---

## Running the Final Notebook

Upload and run:

```text
notebooks/autospectra_end_to_end.ipynb
```

The notebook writes its final artifacts to:

```text
/kaggle/working/autospectra_outputs
```

It can also export:

```text
/kaggle/working/AutoSPECTRA_Artifacts.zip
/kaggle/working/AutoSPECTRA_Flask_Deployment.zip
```

---

## Local Validation

Validate the Week 2 notebook:

```bash
python scripts/validate_week02_notebook.py
```

Run repository tests:

```bash
python -m pytest tests -q
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## GitHub Workflow

Each member should:

1. create a role-specific branch;
2. commit only meaningful incremental work;
3. use descriptive commit messages;
4. open an issue for each task;
5. link the issue to a pull request;
6. request review from another member;
7. record non-code work in Markdown;
8. merge only after review;
9. update the contribution-evidence log.

Example branch:

```bash
git checkout -b week2/amit-data-pipeline
```

Example commit:

```bash
git commit -m "Notebook: add Week 2 HCRL dataset audit and initial EDA"
```

---

## Responsible AI and Safety

AutoSPECTRA follows these principles:

- defensive use only;
- no automatic safety-critical vehicle control;
- human oversight;
- confidence is not treated as certainty;
- false positives and false negatives are reported separately;
- dataset and generalisation limitations are disclosed;
- raw research data is not committed;
- secrets and access tokens are never committed;
- potential dual-use risks are documented;
- model outputs are treated as decision-support evidence.

---

## Known Limitations

- One-vehicle benchmark.
- Balanced samples do not represent natural attack prevalence.
- CAN IDs may create vehicle-specific shortcuts.
- Independent normal capture is not the primary normal source.
- No complete cross-dataset evaluation is included in the stored final run.
- Fusion does not outperform the best standalone tree models.
- The autoencoder misses a substantial proportion of attacks.
- Latency is estimated at window level.
- The prototype has not been tested in a real moving vehicle.
- The system is not safety-certified.

---

## Reproducibility

The project uses:

- fixed random seeds;
- explicit class order;
- versioned split strategy;
- configuration-based processing;
- class-coverage assertions;
- validation-only model selection;
- validation-only anomaly threshold selection;
- test-set isolation;
- saved metrics and plots;
- documented hardware and software versions;
- GitHub issues, commits, reviews and pull requests.

The authoritative class order is:

```text
Normal, DoS, Fuzzy, Gear, RPM
```

---

## Academic and Defensive-Use Disclaimer

AutoSPECTRA is an academic prototype created for research, learning and defensive cybersecurity evaluation.

It is not:

- a commercial automotive security product;
- a certified intrusion-detection system;
- a substitute for expert automotive-security review;
- authorised to inject CAN traffic;
- authorised to control a real vehicle;
- suitable for unsupervised safety-critical decisions.

---

## Project Status

```text
Week 1: Completed
Week 2: Completed
Week 3: Planned / incremental evidence
Week 4: Planned / incremental evidence
Week 5: Planned / incremental evidence
Week 6: Planned / incremental evidence
Week 7: Planned / incremental evidence
Week 8: Planned / final integration
```

The authoritative final implementation is maintained in:

```text
notebooks/autospectra_end_to_end.ipynb
```
