# Week 4 Critical Evaluation and Safety Review

**Owner:** Nagireddy Nakka  
**Role:** Critical Evaluation and Responsible AI Lead

## Safety-Critical Error Interpretation

### False negative

An attack window is classified as Normal. This is especially important because a missed intrusion could allow malicious traffic to continue without an alert.

### False positive

A Normal window is classified as an attack. Excessive false alarms can reduce operator trust and could become unsafe if future systems respond automatically.

## Responsible Interpretation of High Scores

Near-perfect benchmark performance must not be described as proof of real-vehicle readiness.

The main limitations are:

1. one vehicle platform;
2. balanced experimental samples;
3. CAN IDs may encode dataset-specific shortcuts;
4. Normal windows are derived from legitimate frames inside attack captures;
5. no cross-vehicle validation is completed in Week 4;
6. test-set results must not be used to redesign the split.

## Deployment Position

The Week 4 models are academic decision-support baselines. They are not certified automotive security systems and must not trigger automatic safety-critical control.
