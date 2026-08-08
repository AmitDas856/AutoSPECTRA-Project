# Week 3 Leakage and Reproducibility Review

**Owner:** Nagireddy Nakka  
**Role:** Leakage, Ethics and Reproducibility Lead

## Leakage Controls Reviewed

- non-overlapping 64-frame windows;
- source capture retained;
- chronological order retained;
- train, validation and test assigned after source/class sampling;
- test split not used for model design;
- no label or attack flag in the 24 features;
- no attack ratio in model features;
- configuration hash included in cache name;
- class support checked explicitly;
- global row positions retained for audits.

## Reproducibility Controls

- fixed seed;
- fixed class order;
- fixed window size and stride;
- versioned split strategy;
- exported split metadata;
- feature dictionary;
- sequence-channel dictionary;
- recurrence transformation documented;
- validation scripts and tests.
