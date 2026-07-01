# Project Board — AutoSPECTRA (CAN-bus intrusion detection)

> The tutors review this weekly (evidence rule). Move cards across columns; keep commits small and frequent. Mirror this on the GitHub **Projects** tab once the repo is pushed.

## 🔵 To Do (group / Ad only — these need a human)
- [ ] Each member writes their **own** individual report (Parts A–F, max 4 pages)
- [ ] Maheswari: sequence/anomaly comparison model (LSTM **or** autoencoder)
- [ ] Nagireddy: incident-report generator + Streamlit demo dashboard
- [ ] Miftha: lit review to 12–15 verified citations + ethics analysis

## 🟡 Doing
- [ ] Train the headline **CAN-image → CNN** on the real split (first epochs running)
- [ ] Comparison table: baseline vs CNN vs sequence model on the same split
- [ ] Expand lit review to 10–15 papers (`docs/LITERATURE.md` has 9 + a Gemini prompt)

## 🟢 Done
- [x] Repo scaffolded (Week 1)
- [x] **Direction locked: AutoSPECTRA**, mapped to every LO + module block (`docs/PROJECT-PLAN.md`)
- [x] Proposal reframed to Parts A–F (`docs/PROPOSAL.md`)
- [x] **Runnable baseline prototype** — synthetic CAN + injected attacks, 5-class detection + incident report, verified (`src/can_ids.py`)
- [x] Technical review (`docs/LITERATURE.md`), evaluation plan (`docs/EVALUATION.md`), ethics (`docs/ETHICS.md`), pitch outline (`docs/PITCH-OUTLINE.md`)
- [x] Deadline confirmed **18/08/2026**; repo on GitHub, members invited (Week 5)
- [x] **HCRL Car-Hacking dataset** downloaded + loader with per-file **time-ordered split** and leakage assert (`src/data/load_split.py`)
- [x] **Eval harness** — per-class P/R/F1, FPR, ROC-AUC, confusion matrix, detection latency (`eval/run_eval.py`)
- [x] **First real-dataset metrics committed** — Decision Tree + RandomForest baselines (`eval/results_week6.md`)

## Milestones (from the brief)
| Gate | Week | What's due |
|---|---|---|
| Initial proposal | 4 | `docs/PROPOSAL.md` ✓ |
| Progress check | 7 | working detection + first real-dataset metrics |
| Progress check | 10 | full pipeline + ethics + report draft |
| **Pitch (live demo)** | 11/12 | 15-min pitch + 5 Q&A + commented source |
