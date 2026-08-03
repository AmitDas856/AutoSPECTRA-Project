# Initial Ethics and Responsible-AI Risk Register

| Risk | Potential harm | Likelihood | Impact | Initial mitigation | Owner |
|---|---|---:|---:|---|---|
| False negative | A real attack is missed | Medium | Critical | Prioritise per-class recall; analyse missed attacks; human oversight | Evaluation lead |
| False positive | Repeated unnecessary alerts and loss of trust | Medium | High | Measure false-positive rate; avoid automatic vehicle intervention | Evaluation lead |
| Dataset bias | Model learns one vehicle's identifiers rather than general attack behaviour | High | High | State limitation; source-aware evaluation; cross-dataset work as stretch goal | Ethics lead |
| Dual use | Technical material could support offensive misuse | Medium | High | Defensive framing; do not publish exploit instructions; responsible disclosure | Ethics lead |
| Telematics privacy | Real deployment could expose driving behaviour | Medium | High | Local processing; data minimisation; do not collect unnecessary identifiers | UI/reporting lead |
| Confidence misuse | Overconfident score is treated as certainty | Medium | High | Calibration analysis; confidence wording; operator review | Fusion lead |
| Unsafe automation | Alert directly triggers braking, steering or engine action | Low in prototype | Critical | Decision-support only; explicit prohibition in interface and report | All |
| Reproducibility failure | Results cannot be independently checked | Medium | Medium | Config files, seeds, README, environment record and saved metrics | Repo owner |
| Unequal contribution | Individual work is not visible | Medium | High academically | Weekly issues, commits, PRs, reviews and evidence log | All |
