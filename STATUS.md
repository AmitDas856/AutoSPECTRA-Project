# STATUS — Amit (Data + Eval)

**Last updated:** 2026-06-30

## Done (Week 5-6)
- `src/data/load_split.py`: per-file time-ordered 70/30 split, leakage assert ✓
- `data/` wired to four CSVs (Windows junction, git-ignored)
- `eval/run_eval.py`: harness — per-class precision/recall/F1, FPR, ROC-AUC, confusion matrix
- `eval/baseline_rf.py`: Decision Tree baseline, runs on real data
- `eval/results_week6.md`: **first real metrics committed to GitHub** ✓
- `eval/confusion_matrix.png`: confusion matrix on 4.97M test frames ✓

## First real results (Decision Tree, per-file split, 2026-06-30)
| Class | Precision | Recall | F1 |
|---|---|---|---|
| Normal | 1.0000 | 1.0000 | 1.0000 |
| DoS | 1.0000 | 1.0000 | 1.0000 |
| Fuzzy | 0.9999 | 0.9994 | 0.9996 |
| Gear | 1.0000 | 1.0000 | 1.0000 |
| RPM | 1.0000 | 1.0000 | 1.0000 |

Macro ROC-AUC: 0.9999 | FPR all classes < 0.0001

**NOTE:** Near-perfect scores are expected and suspicious — discuss in Part D.

## Split (per-file time-ordered)
| | Train | Test |
|---|---|---|
| Normal | 9,483,390 | 4,754,568 |
| DoS | 566,357 | 21,164 |
| Fuzzy | 448,424 | 43,423 |
| Gear | 528,215 | 69,037 |
| RPM | 572,245 | 82,652 |

All 5 classes in train AND test. Leakage assert passes per-file ✓

## Next session priorities
1. Upgrade Decision Tree to RandomForest (when memory allows)
2. Wire Ad's CNN output through `eval/run_eval.py` — same harness, same split
3. Add detection latency metric (Week 8)
4. Write Part D draft: explain why ~1.0 scores are expected, not impressive

---

# STATUS — CV + Lead

**Owner:** Ad (Aahmad)
**Last updated:** 2026-06-29
**Model used this session:** Claude Sonnet

---

## 1. Done (what works right now)
- Repo live on GitHub (private), Amit invited and accepted
- All 17 issues created on the board, assigned to Ad and Amit (3 members pending GitHub usernames)
- Submission date fixed to 18/08/2026 across all docs
- `src/cv_model.py` — CAN-frame image encoder + TinyCNN, trains one epoch on synthetic data
- `python src/cv_model.py` prints loss and image shape (1, 32, 9) — confirmed working
- Proposal approved by Royce (email 25 Jun); meeting offered after lecture Wed 1 Jul
- GROUP-LOG.md started

## 2. Broken / blocked (what's not working and why)
- 3 team members (Maheswari, Miftha, Nagireddy) haven't provided GitHub usernames — their issues are unassigned
- No real dataset wired yet — waiting on Amit's loader + time-ordered split

## 3. Next step (the single next thing to do)
- Meet Royce after Wed 1 Jul lecture to confirm pitch slot
- Swap in Amit's real data split, train CNN a few epochs, get first real metrics

## 4. How to run what I have
```bash
pip install -r requirements.txt
python src/cv_model.py
```
