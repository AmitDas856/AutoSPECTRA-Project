# Window-size ablation — TinyCNN, WINDOW = 16 / 32 / 64

Run 2026-07-02 with `python src/train_cnn.py 16` and `python src/train_cnn.py 64`
(32 is the week-6 default run). Same net, same 3-epoch recipe, same 36,000-window
capped train sample, same per-file time-ordered split, all metrics through
`eval/run_eval.py`. Test coverage is the full held-out tail in every run.
Per-run detail: `results_cnn_w16.md`, `results_cnn.md` (32), `results_cnn_w64.md`.

| WINDOW | Test windows | Macro-F1 | ROC-AUC (ovr) | Fuzzy precision | Normal FPR | Episodes detected | Worst latency |
|---|---|---|---|---|---|---|---|
| 16 | 310,675 | 0.9533 | 0.9978 | 0.7374 | 0.01849 | 116 / 116 | 14.3 ms (RPM) |
| 32 | 155,337 | 0.9857 | 0.9993 | 0.9010 | 0.00380 | 116 / 116 | 88.2 ms (Fuzzy) |
| 64 | 77,668 | 0.9956 | 0.9994 | 0.9994 | 0.00514 | 116 / 116 | 255.6 ms (Fuzzy) |

## What the dial does (notes for Part D)

1. **Window length is a context-vs-delay trade-off, and the numbers show it
   cleanly.** More frames per window = more context for the conv filters =
   better classification (macro-F1 climbs 0.9533 → 0.9956), but the detector
   can only fire at the end of a window, so the worst-case detection delay
   grows with it (14 ms → 256 ms).
2. **Fuzzy is the class that pays for short windows.** At WINDOW=16 its
   precision collapses to 0.7374 — inside 16 frames, randomised payloads are
   hard to tell from the natural variety of normal traffic, so thousands of
   Normal windows get flagged. By WINDOW=64 the sample is wide enough that the
   confusion essentially disappears (0.9994). This is the same failure mode as
   the week-6 run, amplified and then resolved by context length.
3. **Every attack episode is caught at every setting** — the ablation moves
   *when* detection happens and *how many false alarms* ride along, not
   *whether* attacks are found. For an in-car IDS the deployment question is
   therefore an alarm-budget / reaction-time question, which is the honest
   framing for the report.
4. **Caveats.** The train cap (36,000 windows) keeps the training budget equal
   across runs but is a much smaller fraction of the available windows at
   16 than at 64 (725k vs 181k available). Window labelling is still
   "any injected frame inside" — support counts shift with window size, so
   compare within this table, not against the frame-level baselines.
