# Week 1 Architecture Decision Log

| ID | Decision | Reason | Alternatives considered | Status | Owner |
|---|---|---|---|---|---|
| ADR-001 | Use source-aware chronological splitting | Reduce leakage from temporally adjacent CAN frames | Random stratified split | Proposed | Amit |
| ADR-002 | Keep Random Forest/XGBoost baseline | Transparent and reliable benchmark | Deep learning only | Proposed | Amit |
| ADR-003 | Use recurrence-style image encoding for CNN | Maps traffic windows to a CV-compatible representation | Raw byte image, Gramian field | Proposed | Aahmad |
| ADR-004 | Use LSTM for supervised temporal classification | Models ordered CAN dependencies | GRU, 1D CNN | Proposed | Maheswari |
| ADR-005 | Treat autoencoder as anomaly detector | Reconstruction score does not directly provide five attack classes | Force multiclass mapping | Proposed | Maheswari |
| ADR-006 | Use rule-based report generation initially | Reproducible, controllable and safe | External LLM dependency | Proposed | Miftha |
| ADR-007 | Decision-support only | Prevent unsafe automated intervention | Automatic ECU isolation | Approved principle | All |
