# AutoSPECTRA

**Deep-Learning Intrusion Detection for the Connected Car (CAN Bus)**  
Module: Advanced Artificial Intelligence Projects in Data Science (55-710603)  
Group: 7

## Project purpose

AutoSPECTRA is a defensive, research-oriented AI system for detecting malicious activity in Controller Area Network (CAN bus) traffic. The planned system will classify traffic into:

- Normal
- Denial of Service (DoS)
- Fuzzy injection
- Gear spoofing
- RPM spoofing

The system combines a transparent tabular baseline, a computer-vision branch, a sequence-learning branch, anomaly detection, prediction fusion, and a plain-language security incident report.

## Week 1 status

- [x] Shared project scope documented
- [x] Initial architecture agreed
- [x] Repository structure created
- [x] Roles and responsibilities documented
- [x] Dataset acquisition plan documented
- [x] Initial ethics and risk register created
- [x] GitHub workflow and contribution rules agreed
- [x] Week 1 issues prepared
- [ ] Dataset downloaded locally by each technical contributor
- [ ] First parser smoke test merged

See [`docs/project-management/WEEK1_PUSH_GUIDE.md`](docs/project-management/WEEK1_PUSH_GUIDE.md).

## Architecture

The live GitHub-rendered Mermaid diagram is available in  
[`docs/architecture/system_architecture.md`](docs/architecture/system_architecture.md).

## Repository layout

```text
AutoSPECTRA/
├── .github/                    # Issue and pull-request templates
├── configs/                    # Reproducible experiment configuration
├── data/                       # Data instructions only; large data is ignored
├── docs/                       # Architecture, ethics, literature and meeting evidence
├── models/                     # Model instructions; trained binaries ignored
├── notebooks/                  # Exploration and experiments
├── results/                    # Generated metrics and figures
├── scripts/                    # Re-runnable entry points
├── src/autospectra/            # Production source package
├── tests/                      # Automated checks
├── README.md
├── requirements.txt
└── .gitignore
```

## Team responsibilities

| Member | Primary responsibility | Secondary responsibility |
|---|---|---|
| Amit Das | Data parsing, chronological windowing, loaders and evaluation harness | Repository and GitHub Project Board owner |
| Aahmad Sayeed | CAN-to-image encoding and CNN | Confusion matrices and ROC plots |
| Maheswari Kamireddy | LSTM and autoencoder anomaly detection | Ablation studies |
| Miftha Thahniyath | Incident-report generation and Flask/Streamlit interface | Demonstration rehearsal lead |
| Nagireddy Nakka | Ethics, responsible research and literature review | Cross-dataset evaluation planning |

Roles establish accountability, not isolation. Pull requests must be reviewed by another member.

## Setup

```bash
git clone <REPOSITORY_URL>
cd AutoSPECTRA
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Week 1 validation

```bash
python scripts/check_project_structure.py
python -m pytest -q
```

## Data

The proposed main dataset is the HCRL Car-Hacking dataset. Large datasets, trained models, cache files and generated artifacts must not be committed. See [`data/README.md`](data/README.md).

## Responsible-use statement

AutoSPECTRA is a defensive academic prototype. It must not be used to access, manipulate, disable or interfere with a real vehicle. Predictions are decision-support alerts only and must not automatically control braking, steering, powertrain or other safety-critical functions.
