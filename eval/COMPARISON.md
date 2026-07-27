# Model Comparison — same split, same harness

Updated 2026-07-01. Every number in this table comes from the same evaluation
harness (`eval/run_eval.py`) on the same per-file time-ordered 70/30 split, so
the models are compared fairly. Details for each model are in
`results_week6.md` (baselines) and `results_cnn.md` (CNN).

| Model | Owner | Unit | Macro-F1 | ROC-AUC (ovr) | Worst-class FPR | Attack episodes detected | Worst latency |
|---|---|---|---|---|---|---|---|
| DecisionTree | Amit | frame | 0.9999 | 0.9999 | 0.00012 | 116 / 116 | 0 ms (first frame) |
| RandomForest | Amit | frame | 1.0000 | 1.0000 | 0.00000 | 116 / 116 | 0 ms (first frame) |
| TinyCNN | Ad | 32-frame window | 0.9857 | 0.9993 | 0.00380 | 116 / 116 | 88 ms (Fuzzy) |
| LSTM / autoencoder | Maheswari | sequence | [VERIFY — not run yet] | | | | |

## How to read this table (notes for Part D)

1. **The units are not the same.** The baselines classify single frames; the
   CNN classifies windows of 32 frames. A window is counted as an attack if
   any injected frame is inside it. This means the numbers are not directly
   comparable one to one. The report must state this clearly.
2. **The frame-level baselines are saturated.** A RandomForest reaches 1.0000
   on every metric. This is expected on this dataset, not impressive: the
   injected attacks differ so obviously from normal traffic (fixed CAN ID
   floods, fully random payloads) that a single tree nearly solves the task.
   Published work on this dataset reports the same ~0.99+ region.
3. **The CNN result is the more informative one.** Its Fuzzy precision is
   0.9010: around 380 Normal windows are wrongly flagged as Fuzzy, because
   random payloads resemble the natural variety of normal traffic inside a
   window. This is the kind of error a real in-car IDS would produce, and the
   false-positive cost is the safety-relevant discussion.
4. **Latency.** The baselines flag the first injected frame of every episode.
   The CNN can only decide at the end of a window, so its best case is bounded
   by the window length. All 116 attack episodes in the test tail were
   detected by all three models.
5. **What none of these numbers show:** a different vehicle, a different bus
   load, or a stealthy attacker that imitates normal traffic. Single-vehicle
   bias is the main limitation and belongs in every report.
