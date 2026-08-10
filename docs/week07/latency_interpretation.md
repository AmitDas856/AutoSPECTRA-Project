# Week 7 Detection-Latency Interpretation

**Owner:** Nagireddy Nakka

The notebook estimates:

```text
attack onset inside a window
→ end timestamp of that detected window
```

This is a window-based upper-bound delay.

It does not include:
- capture-device latency;
- CAN interface buffering;
- preprocessing overhead outside measured inference;
- operating-system scheduling;
- UI rendering;
- network transport;
- human response.

It must therefore not be presented as complete real-vehicle response time.
