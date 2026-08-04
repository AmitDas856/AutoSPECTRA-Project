# Week 2 Sequence Requirements

**Owner:** Maheswari Kamireddy  
**Role:** Sequence Data Lead

## Fields Required for Later Sequence Models

- chronological timestamp;
- CAN ID;
- DLC;
- eight consistent payload positions;
- source capture;
- normal or injected-frame flag;
- inter-arrival time calculated without reordering messages.

## Week 2 Checks

- timestamps are numeric;
- source order is retained;
- DLC defines the number of valid payload bytes;
- absent payload positions are distinguishable from valid information through DLC;
- invalid timestamps are counted and reported;
- future sequence inputs must be created after Week 3 split assignment.

## Future Interface

The final LSTM input is expected to use fixed-length chronological windows. The exact `64 × 11` representation belongs to Week 3, while LSTM training belongs to Week 6.
