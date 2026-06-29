# STATUS — Amit (Data + Eval)

**Last updated:** 2026-06-29

## Done this session
- `src/data/load_split.py` written and runs on real HCRL data
- `data/` folder wired to the four CSVs (Windows junction — no copy needed, git-ignored)
- Time-ordered split runs; **leakage assert passes** (`train.max_ts <= test.min_ts`) ✓

## Real dataset numbers (first run — commit these)
| | Frames |
|---|---|
| Total | 16,569,475 |
| Train (70%) | 11,598,632 |
| Test (30%) | 4,970,843 |

**Train class counts:**
- 0 Normal: 9,562,234
- 1 DoS: 292,402
- 2 Fuzzy: 491,847
- 3 Gear: 597,252
- 4 RPM: 654,897

**Test class counts:**
- 0 Normal: 4,675,724
- 1 DoS: 295,119
- ⚠️ Fuzzy, Gear, RPM = 0 in test (see Known Issues below)

## Known issues / next
- **[CRITICAL — discuss in Part D]** Only 2 classes appear in test (Normal + DoS). Fuzzy/Gear/RPM attack frames all fall in the earliest 70% of the merged timeline. Root cause: each HCRL attack file is a separate capture session with its own time range; merging and splitting globally concentrates early attacks in train. Fix: **per-file time-ordered split** (split each CSV at 70/30 independently, then concatenate train splits and test splits). This is a Week 6 task.
- `load_normal_file` unused (Normal rows come from `flag='R'` in attack files — fine for now)
- Detection latency metric: Week 8 (needs model outputs + timestamps)

## Next session priorities
1. Fix the split: per-file 70/30 so all 5 classes appear in test
2. Wire the RandomForest baseline from `src/can_ids.py` to the eval harness in `eval/run_eval.py`
3. Commit first real metric numbers (Week 6 gate)

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
