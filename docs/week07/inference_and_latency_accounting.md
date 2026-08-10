# Week 7 Inference and Latency Accounting

**Owner:** Amit Das

## Fusion Inference Cost

Fusion inference is represented as the sum of:

```text
Random Forest inference
+ Recurrence CNN inference
+ LSTM inference
+ probability-combination overhead
```

This avoids presenting fusion as if combining three models had zero runtime cost.

## Detection-Latency Evidence

The notebook uses metadata created during windowing to estimate:

```text
first injected attack frame
→ end of the correctly detected window
```

The result is an upper-bound window-completion delay.

It is not equivalent to full ECU, operating-system, network, UI or human-response latency.
