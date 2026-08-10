# Week 7 Dataset Bias and Shortcut Learning

**Owner:** Nagireddy Nakka

## Key Concern

If CAN-ID-only or ID+timing feature groups achieve performance close to all 24 features, the model may be learning capture/vehicle-specific identifier patterns.

## Consequences

- strong benchmark performance may not transfer to another vehicle;
- unseen ECUs may use different identifiers;
- stealth attacks may preserve ordinary identifier distributions;
- confidence can remain high even outside the training domain.

## Responsible Conclusion

Week 7 results demonstrate performance on the protected HCRL benchmark. They do not establish universal automotive intrusion detection.
