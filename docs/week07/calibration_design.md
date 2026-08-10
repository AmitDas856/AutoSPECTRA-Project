# Week 7 Temperature Calibration Design

**Owner:** Maheswari Kamireddy

Candidate temperatures:

```text
0.5 to 3.0
51 evenly spaced values
```

For every candidate, fusion validation probabilities are temperature-adjusted and validation log loss is calculated.

The temperature with the minimum validation log loss is selected.

## Governance

- validation probabilities choose the temperature;
- test probabilities are calibrated only after temperature selection;
- test labels do not participate in the search.

Calibration should be assessed with ECE and log loss, separately from macro-F1.
