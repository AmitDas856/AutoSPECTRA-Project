# Week 3 Sequence Representation Review

**Owner:** Maheswari Kamireddy  
**Role:** Sequence Representation Lead

## Shape

```text
64 frames × 11 channels
```

## Channels

1. Normalised CAN ID.
2. Normalised DLC.
3. Eight normalised payload bytes.
4. Log-scaled inter-arrival time.

## Review Checks

- frame order remains chronological;
- all windows contain exactly 64 frames;
- payload padding is interpreted with DLC;
- each channel is finite;
- normalised values remain within `[0,1]`;
- labels and flags are excluded;
- sequence, tabular and metadata rows stay aligned;
- test data is protected.

## Later Use

- Week 6 Bidirectional LSTM classifier.
- Week 6 normal-only LSTM autoencoder.
