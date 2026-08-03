# Component Interface Contracts

## Canonical CAN frame

| Field | Type | Description |
|---|---|---|
| `timestamp` | float | Message timestamp in seconds |
| `can_id` | integer | Arbitration identifier converted from hexadecimal |
| `dlc` | integer | Data length code |
| `data_0` ... `data_7` | integer | Payload bytes, padded only according to documented policy |
| `source_capture` | string | Original file or capture identifier |
| `label` | string | Normal, DoS, Fuzzy, Gear or RPM where available |

## Window object

Each window should contain:

- source capture;
- start and end timestamps;
- ordered CAN IDs;
- ordered payload bytes;
- derived tabular features;
- final window label;
- attack-onset information where available.

## Model output

Every classifier must return:

```text
N x 5 probability array
```

Class order:

```text
Normal, DoS, Fuzzy, Gear, RPM
```

## Fused output

- predicted class;
- calibrated confidence;
- per-class probabilities;
- model names;
- inference time;
- detection-delay estimate.

## Report output

- JSON record;
- plain-language narrative;
- human-oversight warning;
- recommended defensive action;
- no automated safety-critical control.
