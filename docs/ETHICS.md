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

## Gap to fill
Add 2–3 cited sources on automotive-security ethics / responsible disclosure / IDS bias so the section has academic backing, not just reasoning.
