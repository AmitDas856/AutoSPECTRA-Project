# ABSORPTION — slices reassigned 2026-07-02 (Gate 3)

The 3 original owners never started, so their core tasks moved to Ad + Amit (issues #9–17 reassigned on GitHub; plan in `_inbox/CONTINGENCY-PLAN.md`). Everything below is **done and verified in-repo this session, ready to commit**:
- **Ad ← Sequence (#9–11):** `src/seq_model.py` + `src/train_seq.py`; real run macro-F1 **0.9908** (`eval/results_seq.md`); COMPARISON table now has 4 models.
- **Ad ← Ethics 20% (#13–14):** evidence-anchored scaffold + sources in `docs/ETHICS.md` — **Ad still writes the prose** (AITS-2).
- **Amit ← NLP/demo (#15–17):** `src/incident_report.py` (verified) + `src/dashboard.py`; wired into `src/demo.py` (report prints live on alert).
- **Amit ← Literature (#12):** rows 10–14 added to `docs/LITERATURE.md`, all `[VERIFY]` — Amit confirms in Zotero + writes the sentences.

Integrity: code re-owned honestly (run + explained by the committer); no prose faked; no attribution to absent members.

---

# STATUS — Amit (Data + Eval)

**Last updated:** 2026-07-02

## Done (Week 5-6)
- `src/data/load_split.py`: per-file time-ordered 70/30 split, leakage assert ✓
- `data/` wired to four CSVs (Windows junction, git-ignored)
- `eval/run_eval.py`: harness — per-class precision/recall/F1, FPR, ROC-AUC, confusion matrix, **detection latency** (episode onset → first correct flag)
- `eval/baseline_rf.py`: Decision Tree AND RandomForest on the same 20% stratified sample, tested on the full 4.97M-frame tail
- `eval/results_week6.md`: full baseline evidence ✓
- `eval/COMPARISON.md`: **three-model comparison table on the same split** (Week 7 gate deliverable, one week early) ✓
- Ad's CNN reports through my harness — same metrics, same split ✓

## Latest results (2026-07-01, real runs)
| Model | Unit | Macro-F1 | ROC-AUC | Worst FPR | Worst latency |
|---|---|---|---|---|---|
| DecisionTree | frame | 0.9999 | 0.9999 | 0.00012 | 0 ms |
| RandomForest | frame | 1.0000 | 1.0000 | 0.00000 | 0 ms |
| TinyCNN (Ad) | window | 0.9857 | 0.9993 | 0.00380 | 88 ms |

**Frame-level baselines are saturated — a perfect 1.0000 RandomForest is the
"suspicious near-perfect score" EVALUATION.md warns about. That, plus the CNN's
Fuzzy precision of 0.9010, is the Part D discussion. Do not celebrate the 1.0.**

## Split (per-file time-ordered)
| | Train | Test |
|---|---|---|
| Normal | 9,483,390 | 4,754,568 |
| DoS | 566,357 | 21,164 |
| Fuzzy | 448,424 | 43,423 |
| Gear | 528,215 | 69,037 |
| RPM | 572,245 | 82,652 |

All 5 classes in train AND test. Leakage assert passes per-file ✓

## Gotchas learned (worth report/viva material)
- Global merge-then-split left 3 attack classes out of the test set → per-file split
- Windows Python defaults to cp1252 file encoding → results writers use encoding="utf-8"

## Next session priorities
1. Help Maheswari plug the sequence model into the harness (row 4 of COMPARISON.md)
2. Window/feature ablation support for Ad; latency plot for the report
3. Start Part D draft in my own words (split design, why baselines saturate, FPR cost)
4. Stretch: one honest cross-dataset number on ROAD

---

# STATUS — CV + Lead

**Owner:** Ad (Aahmad)
**Last updated:** 2026-07-02

---

## 1. Done (what works right now)
- Repo live on GitHub (private), Amit invited and accepted
- All 17 issues created on the board, assigned to Ad and Amit (3 members pending GitHub usernames)
- Submission date fixed to 18/08/2026 across all docs
- `src/cv_model.py` — CAN-frame image encoder + TinyCNN (smoke test still passes)
- **`src/train_cnn.py` — TinyCNN trained on the REAL per-file split.** Windows of 32 frames, window = attack if any injected frame inside. Trained on 36k capped windows, tested on ALL 155,337 test windows
- **First real CNN numbers (window-level):** macro-F1 0.9857, macro ROC-AUC 0.9993. The interesting bit: **Fuzzy precision 0.9010** — the CNN mistakes some Normal windows for Fuzzy (randomised payloads look like normal traffic variety). Full table in `eval/results_cnn.md`
- Latency: all 116 attack episodes detected, median 0 ms (first window), worst 88 ms (Fuzzy)
- **Window-size ablation done (WINDOW = 16/32/64):** same net/recipe/split, full table + analysis in `eval/ABLATION.md`. Clean context-vs-latency trade-off (F1 0.9533→0.9956, worst latency 14→256 ms); Fuzzy precision is the sensitive number. `train_cnn.py` now takes the window on the CLI: `python src/train_cnn.py 16`
- **Encoding ablation done (grid vs recurrence plot):** grid wins clearly (macro-F1 0.9857 vs 0.8452) — a genuine negative result; the naive recurrence map collapses the per-feature signal. Written up in `eval/ABLATION.md`. `python src/train_cnn.py 32 rec` runs the recurrence variant
- **Fallback demo built (`src/demo.py`):** replays a real capture, flags attacks live in the terminal — the pitch insurance if Streamlit isn't ready. Verified on the Gear capture: 5 episodes flagged live, all attack frames caught, 0 false positives
- Proposal approved by Royce (email 25 Jun); meeting offered after lecture Wed 1 Jul
- GROUP-LOG.md started

## 2. Broken / blocked (what's not working and why)
- 3 team members (Maheswari, Miftha, Nagireddy) haven't provided GitHub usernames — their issues are unassigned
- nothing technical blocked

## 3. Next step (the single next thing to do)
- Chase the 3 missing GitHub usernames; backup work for their slices is staged locally so we're not blocked
- Feed a real detection from demo.py into the incident-report generator (one-line wire-in)
- Consider a WINDOW=48 point if the report wants a smoother ablation curve

## 4. How to run what I have
```bash
pip install -r requirements.txt
python src/cv_model.py      # 10-second smoke test, no data needed
python src/train_cnn.py     # full real-data training run (needs data/ + ~15 min CPU)
```
