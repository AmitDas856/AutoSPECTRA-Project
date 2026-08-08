# Week 3 Window Metadata and Data Lineage

**Owner:** Miftha Thahniyath  
**Role:** Metadata and Data-Lineage Lead

## Metadata Retained per Window

- split;
- class name;
- source capture;
- start timestamp;
- end timestamp;
- global start row;
- attack-frame count;
- attack ratio;
- first attack position;
- estimated latency upper bound;
- dominant CAN ID;
- dominant CAN ID in hexadecimal.

## Purpose

This metadata supports:

- split traceability;
- leakage audits;
- error analysis;
- attack latency analysis;
- incident-report generation;
- Flask display;
- live-demonstration evidence;
- export of auditable CSV and JSON results.

## Safety Rule

Metadata is evidence for human review. It must not be used to trigger automatic safety-critical vehicle control.
