# Week 7 Ablation Plan

**Owner:** Maheswari Kamireddy

## Feature-Group Ablation

Random Forest is retrained using:

1. Timing only.
2. CAN ID only.
3. Payload only.
4. ID + timing.
5. All 24 features.

Compare:
- macro-F1;
- balanced accuracy;
- attack FPR;
- attack FNR;
- training time;
- inference time.

## Window-Size Ablation Plan

```text
32 frames  → lower delay, less context
64 frames  → primary balanced setting
128 frames → more context, higher delay
```

Full 32/64/128 runs require separate Kaggle executions to avoid memory pressure and preserve an independent cache for each configuration.
