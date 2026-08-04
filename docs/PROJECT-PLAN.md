# AutoSPECTRA — Project Plan (LOCKED 2026-06-18)

**Deep-Learning Intrusion Detection for the Connected Car (CAN bus).**

> The SPECTRA concept (deep learning for embedded security) re-aimed from risky over-the-air EM side-channels onto the car's internal network — where the data is public, the demo is safe, and it merges with your RSC fraud topic and NOMAD. Same sophistication, none of the RF gamble.

## One-liner
A car's electronic control units talk over the **CAN bus**, which has no built-in security. AutoSPECTRA uses deep learning to **detect intrusions and spoofing attacks on live CAN traffic in real time**, then auto-writes a security-incident report. Runs on a laptop, on a real public dataset.

## Why this is the right project for you
- **Solo-feasible.** Public dataset (HCRL Car-Hacking), no hardware, no RF, no specialist-skill dependency. You confirmed the group has no RF skills — this removes that risk entirely.
- **Merges your threads.** Cars (your domain + RSC topic) + embedded security (the SPECTRA appeal) + deep learning + on-device/offline (NOMAD). It even reuses the CAN-bus anomaly-detection papers already in your RSC lit review.
- **Demo gravity, de-risked.** "Watch it catch a live attack injected into a real car's network" is a strong demo that actually works, because it replays recorded data — no anechoic chamber required.

## Architecture (three layers = three module blocks)
```
CAN log → parse frames → ┬─ (CV)  frames → recurrence-plot / grid IMAGE → CNN classifier
                         ├─ (seq) arbitration-ID + payload sequence → LSTM / autoencoder
                         └─ fuse → attack? which class? → (NLP) auto-generated incident report
```
- **CV layer (Block 2):** convert CAN frames to images (recurrence plots, à la *Rec-CNN*) → CNN. This is the published, legitimate computer-vision component.
- **Sequence/anomaly layer:** LSTM or autoencoder on the ID/payload stream (the survey says LSTM hits ~0.999 on this dataset).
- **NLP layer (Block 3):** generate a plain-language security report ("DoS injection detected on ID 0x316 at t=12.4s; 412 anomalous frames; confidence 0.97").

## Datasets (free, public)
- **HCRL Car-Hacking** — 1.3M messages from a real 2010 Hyundai Sonata; classes: normal, DoS, Fuzzy, Gear-spoof, RPM-spoof. Primary.
- **ROAD (Oak Ridge)** — alternative/cross-check.
- The prototype ships with a **synthetic CAN generator + injected attacks** so it runs before you download anything.

## Does it cover the brief? Yes — full map
| Brief requirement | Weight | How AutoSPECTRA covers it |
|---|---|---|
| LO1 Knowledge & Techniques | 10% | CNN (on trace-images), LSTM/GRU (sequences), autoencoder (unsupervised anomaly); benchmarked vs published ~99% |
| LO2 Design & Implementation | 10% | End-to-end pipeline: parse → feature/image → model → live detector + report |
| LO3 Technical & Critical Evaluation | **30%** | Per-class precision/recall/F1, ROC-AUC, confusion matrix, detection latency; supervised vs anomaly comparison; honest limits (single-vehicle dataset → generalisation) |
| LO4 Ethics & Responsible Research | **20%** | Dual-use (IDS knowledge ↔ attack), automotive *safety*-critical harm, telematics privacy, dataset bias, responsible disclosure |
| Block 1 — Project Setup & Delivery | — | GitHub evidence rule, board, README, PM |
| Block 2 — Computer Vision & GenAI | — | CAN-frame → image → CNN (CV); generative incident report |
| Block 3 — NLP | — | Auto-written security report grounded in the detections |
| Group source code + mandatory README | — | Runnable repo; README covers setup/run/data |
| Live pitch demo | **30%** | Stream a CAN log → live attack flagging on a dashboard → report. Reproducible, solo, no hardware |

**Verdict:** covers every learning outcome and all three blocks, including the CV and NLP blocks a plain classifier would miss. Locked.

## Scope guard (keep it demoable, solo)
MVP = detect the 5 Car-Hacking attack classes on a held-out split, show it live on a Streamlit dashboard, generate one report. CNN-on-images is the headline model; LSTM/autoencoder is the comparison. Everything else (real hardware capture, multi-vehicle, the EM side-channel stretch) is **"Future Work."**

## For the group / Royce (continuity, not a restart)
"We focused our embedded-security idea onto the car's CAN bus: a real public dataset, a safe live demo, and the same deep-learning + security core. It also lets each of us own a clean layer (CV model / sequence model / data+ethics / report+UI)." This protects the GitHub continuous-engagement score — it's an evolution of the SPECTRA pitch, and it gives the SPECTRA proposer a clear role (lead the CV/CNN model).
