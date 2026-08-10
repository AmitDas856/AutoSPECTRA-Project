# Bidirectional LSTM Design

**Owner:** Maheswari Kamireddy

```text
64 × 11 sequence
→ Bidirectional LSTM, hidden size 64
→ mean pooling
→ LayerNorm
→ Dropout 0.25
→ Linear 128→5
```

Training uses class-weighted cross-entropy, label smoothing, AdamW, weight decay, gradient clipping and validation macro-F1 checkpoint selection.
