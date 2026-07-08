# Project Board — AutoSPECTRA (CAN-bus intrusion detection)

> The tutors review this weekly (evidence rule). Move cards across columns; keep commits small and frequent. Mirror this on the GitHub **Projects** tab once the repo is pushed.

> **2026-07-02 — slices reassigned.** The three original owners (Maheswari, Miftha, Nagireddy) never started. Their core tasks were absorbed into Ad + Amit so the project is not compromised (see `_inbox/CONTINGENCY-PLAN.md`, Gate 3). Issues #9–17 reassigned on GitHub. Code re-owned honestly — whoever commits it can explain it in the viva.

## 🔵 To Do (group / Ad + Amit)
- [ ] Each member writes their **own** individual report (Parts A–F, max 4 pages)
- [ ] Ad: write the Ethics 20% prose from the scaffold (#13, #14) — do NOT ship the scaffold as-is
- [ ] Amit: verify literature rows 10–14 in Zotero, write the critical sentences (#12)
- [ ] Amit: run + screenshot the Streamlit dashboard for the pitch deck (#16)

## 🟡 Doing
- [x] Train the headline **CAN-image → CNN** on the real split — done (`eval/results_cnn.md`)
- [x] Comparison table: baseline vs CNN vs **LSTM** on the same split — done (`eval/COMPARISON.md`, 4 models)
- [ ] Ad (absorbed #9–11): SeqLSTM in `src/` + comparison row — **done, ready to commit**
- [ ] Amit (absorbed #15–17): incident-report generator + dashboard in `src/`, wired into demo — **done, ready to commit**
- [ ] Expand lit review to 12–15 papers — rows 10–14 added as [VERIFY] (`docs/LITERATURE.md`)

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
