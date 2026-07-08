# Ethics & Responsible Research  *(Report Part D · LO4 = **20%**)*

> 20% on its own. The rubric rewards "profound, nuanced evaluation… at the forefront of responsible AI." Tie every point to *our specific system* (a CAN-bus intrusion detector), not AI in general. This domain is unusually rich — use it.

## 1. Dual-use — the core tension
An intrusion *detector* and an intrusion *tool* are two sides of one coin: understanding attacks well enough to detect them means documenting how they work. Discuss **responsible disclosure** (we use a public dataset and do not release attack tooling), and the ethics of publishing automotive-attack capability. This is a genuine, current debate in vehicle security.

## 2. Safety-critical error asymmetry — the high-marks point
This is not spam filtering; it is a moving car.
- **False negative** (missed attack) → a real intrusion proceeds (spoofed brakes/gauges). Potentially fatal.
- **False positive** (false alarm) → driver distrust, or an automated response that is itself unsafe.
These harms are asymmetric and context-dependent; argue how your metric choice (recall-weighted? human-in-the-loop alerting?) reflects that. Most student reports miss this — it is where the Distinction marks are.

## 3. Privacy of vehicle/telematics data
CAN and telematics data can reveal driving behaviour, routes and identity. An IDS that phones home, or a dataset that is re-identifiable, raises GDPR-style concerns. Our design keeps detection **on-device** (no data leaves the car) — a defensible privacy-by-design choice.

## 4. Bias & generalisation
The Car-Hacking dataset is **one 2010 Hyundai Sonata**. A model trained on it may fail silently on other makes, newer buses (CAN-FD, Automotive Ethernet), or unseen attacks — giving **false confidence**, which in a safety system is its own harm. Investigate and state this honestly (the rubric explicitly rewards "bias is investigated and findings discussed").

## 5. Accountability & responsible research
- Who acts on a flag — the car, the driver, the manufacturer? Liability is unresolved; frame the tool as decision-support with a human in the loop.
- **AITS declaration** (required appendix) kept honest via `AI-USE-LOG.md`; respect the dataset licence.

## Map to the rubric (LO4, 20%)
| Rubric phrase | Our evidence |
|---|---|
| "bias is investigated and findings discussed" | §4 single-vehicle generalisation tests |
| "independent insight / forefront of responsible AI" | §1 dual-use + §2 safety-critical error asymmetry |
| "evaluation of ethical responsibilities" | privacy-by-design (§3), accountability/human-in-loop (§5) |

## Working scaffold — evidence anchors + sources (Ad absorbs Ethics, 2026-07-02)

> Structure and evidence only. **Ad writes the prose himself** (AITS-2) and defends it in the viva. The value here is that every theme is anchored to a real number from our own `eval/`, which is where the Distinction marks are. Four-move pattern per theme: (1) the issue for *our* system → (2) cite a source → (3) point at our own number → (4) what we did about it.

| Theme | Anchor to OUR real result | Source to cite (verify in Zotero) |
|---|---|---|
| §1 Dual-use / disclosure | public dataset only; no attack tooling or new vuln released | UN Reg. No. 155 / UNECE WP.29 (CSMS + mandatory attack reporting) [VERIFY] |
| §2 Safety error asymmetry (**the 20% point**) | window ablation: Normal FPR 0.0038 (w32) → **0.0185 (w16)** in `eval/ABLATION.md`; CNN Fuzzy precision 0.9010 = real false-alarm cost; RandomForest FPR 0.0 is the *saturated* benchmark, not a win | argue human-in-loop + recall-weighting from our own numbers |
| §3 Privacy | detection is on-device (no telematics leaves the car) = privacy-by-design | GDPR data-minimisation principle [VERIFY] |
| §4 Bias / generalisation | one 2010 Hyundai only; the per-file-split gotcha (3 classes vanished from the global test) in `eval/results_week6.md` is a concrete "dataset structure biases results" example | ACM CSCS '22 dataset-eval + ROAD (CSCS '24) [VERIFY] — see LITERATURE rows 10–11 |
| §5 Accountability | incident report is template-based, not an LLM — deterministic, auditable, cannot hallucinate a fact the detector didn't report (`src/incident_report.py`) | frame as decision-support, human-in-loop |

Extra angle now available: the LSTM-vs-CNN result (LSTM Fuzzy precision 0.9737 vs CNN 0.9010) shows model choice changes the false-alarm profile — another concrete, evidenced ethics point about which model you deploy in a safety system.

Full bullet outline with the argument moves: was staged in `_inbox/miftha-ethics-lit/ethics-outline.md` (kept for reference).
