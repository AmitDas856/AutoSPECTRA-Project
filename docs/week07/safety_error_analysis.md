# Week 7 Safety Error Analysis

**Owner:** Nagireddy Nakka  
**Role:** Responsible AI, Latency and Critical Evaluation Lead

## False Negative

An attack window is predicted as Normal.

Risk:
- malicious traffic can continue without an alert;
- high confidence can create false reassurance.

## False Positive

A Normal window is classified as an attack.

Risk:
- repeated false alarms reduce trust;
- unsafe human or automated reactions may follow.

Week 7 therefore reports both attack FPR and attack FNR for every multiclass model.
