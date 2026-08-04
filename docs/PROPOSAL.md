# Project Proposal — AutoSPECTRA (CAN-bus Intrusion Detection)

> Skeleton aligned to the Individual Report's Parts A–F (70%, max 4 A4 pages). Shared project facts live here; **each member writes their own report prose** (don't submit identical text — integrity risk).

## Part A — Introduction: problem & importance
Modern vehicles run dozens of electronic control units (ECUs) that communicate over the **Controller Area Network (CAN)**. CAN was designed for reliability, **not security**: messages are broadcast with no authentication or encryption, so any node that gains access can inject or spoof frames. Demonstrated attacks (DoS, fuzzing, gear/RPM spoofing) can disable brakes or falsify dashboard readings — a **safety-critical** problem as cars become more connected. AutoSPECTRA detects these intrusions in real time using deep learning and reports them in plain language. Beneficiaries: vehicle manufacturers, fleet operators, security researchers, and (tying to my RSC work) used-car buyers exposed to tampered ECUs.

## Part B — Technical review (AI/DS techniques explored) → see `LITERATURE.md`
- Signature vs **anomaly-based** intrusion detection; why ML beats fixed rules on zero-day attacks.
- **CNN on image-encoded CAN traffic** (recurrence plots / grid images — *Rec-CNN*): the computer-vision route.
- **Sequence models** (LSTM/GRU) and **autoencoders** for unsupervised anomaly detection on the ID/payload stream.
- Benchmarks on the Car-Hacking dataset (~0.99 accuracy in the literature) — our results are directly comparable.

## Part C — Design & implementation
Pipeline: `CAN log → parse frames → {image-encode → CNN | sequence → LSTM/autoencoder} → fuse → classify attack → NLP incident report`. See `src/can_ids.py`. Modular so members own clean components (data+eval / CV model / sequence model + report + UI). Dataset: HCRL Car-Hacking (real vehicle, 5 attack classes); synthetic generator included for development.

## Part D — Evaluation (technical + social/ethical) → see `EVALUATION.md`, `ETHICS.md`
- **Technical:** per-class precision/recall/F1, ROC-AUC, confusion matrix, **detection latency** (must be fast enough to matter on a moving car); supervised vs anomaly-based comparison.
- **Ethical:** **dual-use** (the same model that defends could profile attacks), automotive **safety** harm of false negatives, **telematics privacy**, **dataset bias** (one 2010 Hyundai → does it generalise?), responsible disclosure.

## Part E — Project management & future work
- Roles + the GitHub board + commit cadence as the evidence trail.
- **Future work:** a real hardware capture from an OBD-II port; multi-vehicle generalisation; and the **EM side-channel** extension (the original SPECTRA idea) as an advanced research direction once the software baseline is proven.

## Part F — Conclusion
A working, evaluated, laptop-class intrusion detector for the car network, with an honest account of where it succeeds and fails — and a clear path to real-world deployment.

## Scope guard (keep it demoable, solo-feasible)
MVP = detect the 5 Car-Hacking attack classes on a held-out split, shown live on a dashboard, with one generated report. CNN-on-images is the headline; LSTM/autoencoder is the comparison. Hardware capture, multi-vehicle, and EM side-channels are **Future Work**. No GPU required.
