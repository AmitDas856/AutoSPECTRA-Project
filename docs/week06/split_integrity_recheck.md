# Week 6 Split Integrity Recheck

**Owner:** Amit Das

Before training:
- confirm the versioned cache uses the Week 3 split;
- confirm all sequences contain 64 frames and 11 channels;
- confirm all five classes exist in the supervised splits;
- confirm the autoencoder receives only Normal training windows;
- confirm validation contains Normal and attack windows;
- keep the test split isolated until final evaluation.
