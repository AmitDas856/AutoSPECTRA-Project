# Week 3 Windowing and Split Implementation

**Owner:** Amit Das  
**Role:** Windowing, Split and Integration Lead

## Windowing

- Window size: 64 frames.
- Stride: 64 frames.
- Overlap: none.
- Normal label: no injected frame.
- Attack label: at least one injected frame from the source capture.

## Split Strategy

The implementation uses:

> Source-aware, class-aware, chronologically partitioned reservoir sampling.

Candidate windows are sampled across the full source/class timeline. Each group is then sorted by original row position and divided into 70% training, 15% validation and 15% testing.

Balancing is applied only after the chronological partitions exist.

## Leakage Controls

- no shared-frame overlap;
- original source capture retained;
- global start-row position retained;
- test set protected;
- target labels excluded from features;
- attack ratio retained as metadata only;
- configuration-versioned cache;
- all classes required in every split.

## Week Boundary

No classifier is trained in Week 3.
