# Project Board — AutoSPECTRA (CAN-bus intrusion detection)

> The tutors review this weekly (evidence rule). Move cards across columns; keep commits small and frequent. Mirror this on the GitHub **Projects** tab once the repo is pushed.

## 🔵 To Do (group / Ad only — these need a human)
- [ ] **Pitch AutoSPECTRA to the group** (`docs/PROJECT-PLAN.md`) + agree layers/roles
- [ ] Confirm the deadline with **Royce Copley** — brief says **xx/xx/2026**, genuinely unset
- [ ] Push this repo to GitHub, invite members, assign roles in README
- [ ] Download the **HCRL Car-Hacking dataset** (free) and wire the loader into `src/can_ids.py`
- [ ] Each member writes their **own** individual report (Parts A–F, max 4 pages)

## 🟡 Doing
- [ ] Train the headline **CAN-image → CNN** model + an **LSTM/autoencoder** comparison
- [ ] Build a small **Streamlit** dashboard for the live demo
- [ ] Expand lit review to 10–15 papers (`docs/LITERATURE.md` has 9 + a Gemini prompt)

## 🟢 Done
- [x] Repo scaffolded (Week 1)
- [x] **Direction locked: AutoSPECTRA**, mapped to every LO + module block (`docs/PROJECT-PLAN.md`)
- [x] Proposal reframed to Parts A–F (`docs/PROPOSAL.md`)
- [x] **Runnable baseline prototype** — synthetic CAN + injected attacks, 5-class detection + incident report, verified (`src/can_ids.py`)
- [x] Technical review (`docs/LITERATURE.md`), evaluation plan (`docs/EVALUATION.md`), ethics (`docs/ETHICS.md`), pitch outline (`docs/PITCH-OUTLINE.md`)

## Milestones (from the brief)
| Gate | Week | What's due |
|---|---|---|
| Initial proposal | 4 | `docs/PROPOSAL.md` ✓ |
| Progress check | 7 | working detection + first real-dataset metrics |
| Progress check | 10 | full pipeline + ethics + report draft |
| **Pitch (live demo)** | 11/12 | 15-min pitch + 5 Q&A + commented source |
