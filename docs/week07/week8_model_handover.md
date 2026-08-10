# Week 8 Model Handover

**Owner:** Miftha Thahniyath

Week 8 receives:

- final class order;
- principal multiclass model name;
- Random Forest fallback;
- fusion weights;
- calibration temperature;
- inference requirements;
- model-selection evidence;
- human-oversight rules.

## Week 8 Application Rule

The Flask/demo layer must not claim that fusion is the strongest model unless Week 7 results show that.

If Random Forest remains the best standalone model, it should remain the principal fallback for the live demonstration.

Controlled incident reports must preserve:

```text
human oversight required
no automatic vehicle control
```
