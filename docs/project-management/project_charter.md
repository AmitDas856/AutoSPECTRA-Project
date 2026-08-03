# AutoSPECTRA Project Charter

## Project title

AutoSPECTRA: Deep-Learning Intrusion Detection for the Connected Car

## Problem

Controller Area Network communication was designed for reliable, low-latency in-vehicle communication rather than modern cybersecurity. CAN messages are broadcast without native sender authentication or encryption. A compromised component may therefore inject or spoof traffic that other electronic control units trust.

## Project aim

Design and critically evaluate an AI-assisted intrusion-detection prototype that classifies normal and malicious CAN traffic and generates an understandable incident report while respecting safety, privacy, responsible research and human oversight.

## Initial research questions

1. How effectively can feature-based, image-based and sequence-based models distinguish Normal, DoS, Fuzzy, Gear-spoofing and RPM-spoofing traffic?
2. Does calibrated late fusion improve macro-F1 and attack recall without unacceptable false-positive rates or latency?
3. What technical, ethical and generalisation limitations prevent immediate deployment in real vehicles?

## Week 1 scope

Included:

- repository and workflow setup;
- dataset-access plan;
- architecture design;
- initial evaluation plan;
- initial ethics and dual-use assessment;
- module-to-project mapping;
- work allocation;
- parser interface definition.

Excluded from Week 1:

- final model training;
- final performance claims;
- real vehicle integration;
- automated safety intervention;
- production deployment.

## Success criteria for the final project

- Reproducible data-processing pipeline.
- Leakage-resistant evaluation.
- At least one transparent baseline and one deep-learning model.
- Five-class metrics with per-class support.
- Live analysis of unseen CAN traffic.
- Plain-language and structured incident reports.
- Documented latency, false alarms and model limitations.
- Responsible-use and ethics analysis.
- Complete GitHub contribution evidence.
