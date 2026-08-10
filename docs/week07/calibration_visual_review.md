# Week 7 Calibration Visual Review

**Owner:** Aahmad Sayeed

## Visual Evidence Reviewed

- CNN reliability diagram;
- uncalibrated fusion reliability diagram;
- calibrated fusion reliability diagram;
- validation temperature-search curve;
- expected calibration error before/after scaling;
- ROC and precision–recall plots.

## Interpretation

Calibration should not be described as improving classification unless predicted classes actually change.

Temperature scaling is primarily evaluated using:

- validation log loss for selection;
- test ECE and log loss for final reporting.

Macro-F1 must remain a separate classification metric.
