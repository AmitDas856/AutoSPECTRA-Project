# AutoSPECTRA Incident-Report Schema

## Purpose

The reporting layer converts structured model output into a controlled, human-readable security incident report. It does not invent evidence and does not issue autonomous vehicle-control commands.

## Structured JSON Schema

```json
{
  "system": "AutoSPECTRA",
  "model": "Calibrated RF + CNN + LSTM Fusion",
  "predicted_class": "DoS",
  "confidence": 0.97,
  "severity": "High",
  "window_start_timestamp": 1478201000.10,
  "window_end_timestamp": 1478201000.14,
  "window_size_frames": 64,
  "dominant_can_id": "0x000",
  "message_rate_hz": 1800.0,
  "unique_can_ids": 4,
  "id_entropy_bits": 0.72,
  "anomalous_frames": 58,
  "recommended_action": "Alert the operator and inspect the affected CAN segment.",
  "human_oversight": "Decision-support alert only. Do not automatically control braking, steering, engine, transmission, or other safety-critical functions."
}
```

## Required Fields

| Field | Meaning |
|---|---|
| `system` | System name |
| `model` | Model or fusion configuration |
| `predicted_class` | Normal, DoS, Fuzzy, Gear or RPM |
| `confidence` | Calibrated confidence where available |
| `severity` | Informational, Low, Medium, High or Critical |
| `window_start_timestamp` | Start of analysed window |
| `window_end_timestamp` | End of analysed window |
| `window_size_frames` | Number of CAN frames |
| `dominant_can_id` | Most frequent CAN ID |
| `message_rate_hz` | Approximate traffic rate |
| `unique_can_ids` | Number of distinct identifiers |
| `recommended_action` | Defensive human-reviewed action |
| `human_oversight` | Mandatory safety statement |

## Severity Rules

Initial symbolic mapping:

| Prediction | Initial severity |
|---|---|
| Normal | Informational |
| Fuzzy | Medium |
| Gear spoofing | High |
| RPM spoofing | High |
| DoS | High |

Severity may also consider confidence, message rate and anomaly duration. Any rule changes must be documented.

## Narrative Template

Example:

```text
AutoSPECTRA analysed a 64-frame CAN window ending at [timestamp].
The [model] classified the traffic as [class] with [confidence] confidence.
The window contained approximately [rate] messages per second and
[unique IDs] unique CAN identifiers. The dominant identifier was [CAN ID].
Recommended action: [action]. This is a decision-support alert and must not
automatically control a safety-critical vehicle function.
```

## Reporting Constraints

- Do not state that an attack is confirmed when the confidence is low.
- Do not hide model uncertainty.
- Do not generate vehicle-control commands.
- Do not reveal unnecessary offensive instructions.
- Preserve the original timestamps and evidence.
- Mark anomaly-only autoencoder results as anomalies, not confirmed attack classes.
