# AutoSPECTRA — Deep-Learning Intrusion Detection for the Connected Car (CAN bus)

> **Module:** Advanced AI Projects in Data Science (55-710603) · **Pitch:** Week 11/12 (live demo) · **Report:** 70% (max 4pp) · **Pitch:** 30%
> **One-liner:** the car's internal network (CAN bus) has no security. AutoSPECTRA uses deep learning to **detect intrusion and spoofing attacks on live CAN traffic in real time**, then auto-writes a security-incident report. Real public dataset, runs on a laptop, no hardware. *(Evolution of our SPECTRA pitch — embedded security + deep learning, re-aimed from risky EM side-channels onto the car network. See `docs/PROJECT-PLAN.md`.)*
>
> **Grade levers (from the brief):** Technical Evaluation **30%** + Pitch/Communication **30%** + Ethics **20%** = **80%**. Implementation is only **10%**. Build a modest model that works, then pour effort into evaluation, ethics, and the pitch. Deadline: **18/08/2026 (live pitch Week 11/12).**

## Why this project
It covers all three module blocks: **Computer Vision** (CAN frames → images → CNN), **NLP** (auto-generated incident report), and a strong **deep-learning evaluation** on a real benchmark. The live demo (watch it catch an attack injected into a real car's traffic) works reliably because it replays a recorded dataset — no anechoic chamber, no RF. Safety-critical automotive security gives an exceptional ethics story (dual-use, responsible disclosure). Full brief-coverage map in `docs/PROJECT-PLAN.md`.

## The 🔴 rule we live by
> *"Work not documented on GitHub is considered non-existent."* — the module's evidence rule.
Every member commits regularly (no end-of-term code dumps), the Project Board moves cards To Do → Doing → Done, and research/design notes go in `docs/`. See `PROJECT_BOARD.md`.

## Repo map
```
project-repo/
├── README.md            ← this
├── PROJECT_BOARD.md     ← the Kanban the tutors check weekly
├── requirements.txt
├── docs/
│   ├── PROJECT-PLAN.md  ← LOCKED scope + full brief-coverage map
│   ├── PROPOSAL.md      ← Report Parts A–F skeleton
│   ├── LITERATURE.md    ← technical review citations (Part B)
│   ├── EVALUATION.md    ← metrics + protocol (Part D, 30%)
│   ├── ETHICS.md        ← responsible-AI analysis (Part D, 20%)
│   ├── PITCH-OUTLINE.md ← 15-min pitch + live-demo script (30%)
│   └── AI-USE-LOG.md    ← declared AI assistance (integrity)
├── eval/                ← evaluation harness + labelled test data
└── src/
    └── can_ids.py       ← runnable prototype (synthetic CAN + injected attacks; swap in Car-Hacking)
```

## Architecture (three layers = three module blocks)
```
CAN log → parse → ┬─ (CV)  frames → recurrence-plot / grid IMAGE → CNN
                  ├─ (seq) ID + payload sequence → LSTM / autoencoder
                  └─ fuse → attack? which class? → (NLP) auto incident report
```
Primary dataset: **HCRL Car-Hacking** (~16.6M CAN frames across the four attack captures, logged from a real Hyundai YF Sonata via OBD-II, 5 classes). Prototype ships with a synthetic CAN generator so it runs before any download.

## Team (assign by layer — gives the SPECTRA proposer the CNN role)
| Member | Suggested role | GitHub |
|---|---|---|
| Ad (35066639) | data pipeline + evaluation | @ |
| _SPECTRA proposer_ | CV model (CAN→image CNN) | @ |
| _teammate_ | sequence/anomaly model + NLP report + UI | @ |

## Run (synthetic data — works with no download, no GPU)
```bash
pip install -r requirements.txt
python src/can_ids.py --demo          # generate CAN traffic + attacks, train, evaluate
python src/cv_model.py                # 10-second CNN smoke test, no data needed
```

## Get the data (HCRL Car-Hacking)
The real experiments need the dataset. It is free but not committed to this repo.

1. Download from the HCRL page: https://ocslab.hksecurity.net/Datasets/car-hacking-dataset
2. The four files the loader uses are `DoS_dataset.csv`, `Fuzzy_dataset.csv`, `gear_dataset.csv` and `RPM_dataset.csv`. The normal-run file is not used yet — Normal frames come from the R-flagged rows inside the attack captures.
3. Place the CSVs in a `data/` folder at the repo root. The `data/` folder is git-ignored, so the CSVs are never committed. A Windows junction to wherever the download lives also works:
   `New-Item -ItemType Junction -Path data -Target "<your dataset folder>"` (PowerShell)
4. Check the data loads: `python src/data/load_split.py` should print the per-file split and the class counts (about 16.57M frames in total, all 5 classes present in train and test).
5. Then the real runs work: `python src/train_cnn.py` (CNN) and `python eval/baseline_rf.py` (baselines).

## Assessment mapping
Report **A** problem → `docs/PROPOSAL` · **B** technical review → `docs/LITERATURE` · **C** design/impl → `src/` · **D** evaluation → `docs/EVALUATION` + `docs/ETHICS` · **E** project mgmt → `PROJECT_BOARD` + commit history · **F** conclusion → report. Full LO/block map: `docs/PROJECT-PLAN.md`.
