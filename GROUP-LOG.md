# GROUP LOG — AutoSPECTRA weekly heartbeat
(Each member appends a 4-line block by Sunday night. Ad reads this to run the project.)

## Week 5 — Ad (CV + Lead)
- Done: repo on GitHub, team invited, board up, CNN encoder running on synthetic data
- Blocked: nothing
- Next: swap in Amit's real split, train a few epochs
- AI: Claude tutored the image-encoder; I wrote/edited and understand it

## Week 5/6 — Amit (Data + Eval)
- Done: HCRL loader + per-file time-ordered split (leakage assert passes); eval harness with per-class P/R/F1, FPR, ROC-AUC, confusion matrix, detection latency; DT + RF baseline numbers on the full 4.97M-frame test tail committed
- Blocked: nothing (global split had 3 classes missing from test — fixed with per-file split, documented for Part D)
- Next: comparison table baseline vs CNN vs sequence model; Part D draft
- AI: Claude assisted with loader/harness scaffolding and Windows debugging; reviewed line-by-line, logged in AI-USE-LOG

## Week 6 — Ad (CV + Lead)
- Done: TinyCNN wired to the real split via windowing (`src/train_cnn.py`); first real CNN numbers in `eval/results_cnn.md`
- Blocked: nothing
- Next: window-size + encoding ablation; feed detections to Nagireddy's report generator
- AI: Claude assisted wiring data windows into the encoder; logged in AI-USE-LOG
