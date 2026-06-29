# Pitch Outline — AutoSPECTRA  *(Group Pitch = **30%** · 15 min + 5 Q&A · Week 11/12)*

> Graded as heavily as the entire technical evaluation. The brief is explicit: the **live demo is the most important part** — "Run your code. Input new data. Show the output." Our demo replays a recorded CAN dataset, so it works reliably (no hardware to fail).

## Timing (the brief's required shape)
| Segment | Time | Content | Owner |
|---|---|---|---|
| The Problem | 2–3 min | Hook: the car's network (CAN) has **no security**; demonstrated attacks can spoof gauges or disable brakes. As cars connect, this is safety-critical. | _member_ |
| Your Solution | 2–3 min | "AutoSPECTRA: deep learning that watches CAN traffic and flags intrusions in real time." One architecture diagram (image-CNN + sequence model + report). | _member_ |
| **LIVE Demo** | **5–7 min** | Replay a clean CAN log → all green. Inject a DoS/spoof attack → the model flags it live on the dashboard, names the class, and **auto-writes the incident report**. | _member (rehearsed)_ |
| Evaluation & Impact | 3–5 min | Headline: per-class F1 + detection latency. One ethics point: the false-negative-vs-false-positive **safety asymmetry**. | _member_ |
| The Future | 2 min | The "ask": real OBD-II hardware capture, multi-vehicle generalisation, and the EM side-channel extension. | _member_ |

## Live demo script (de-risk it)
1. Pre-load the dataset and the trained model **before** you present.
2. Show normal traffic first (baseline = all clear) so the attack contrast lands.
3. Inject the attack from a held-out slice → the dashboard flags it, shows the class + confidence, prints the report.
4. **Fallback:** if anything stalls, `python src/can_ids.py --demo` runs the whole pipeline in one command and prints metrics + a report. Never show a stack trace.
5. Record a backup screen-capture the night before as insurance — but present live (the brief forbids relying on video).

## Slides (~8–10, visuals over text)
1. Title + team. 2. The problem (a car + an attacker). 3. Solution one-liner. 4. Architecture (`CAN → image→CNN / sequence→LSTM → attack class → report`). 5. **DEMO** (switch to the dashboard/terminal). 6. Evaluation: per-class F1 + ROC + latency. 7. Ethics: the safety error-asymmetry. 8. Future work / the ask. 9. Repo + thanks.

## Q&A prep (anticipate)
- "Isn't 99% on Car-Hacking already solved?" → yes on that dataset; our contribution is the **critical evaluation** (generalisation, latency, false-positive cost) + the CV encoding + report layer.
- "Would it run on a real ECU?" → CPU inference time numbers; that's our future-work path.
- "How is this not just an attack tool?" → dual-use + responsible disclosure (see `ETHICS.md`).
- "Who did what?" → point at the GitHub contributors graph.

## Per-member individual report
Pitch is group; the **70% report is individual** (max 4 A4 pages). Each member writes their own Parts A–F from the shared `docs/`, differentiated by their layer (data+eval / CV model / sequence model + report). Do **not** submit identical reports.
