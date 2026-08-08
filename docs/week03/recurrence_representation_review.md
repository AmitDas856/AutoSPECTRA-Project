# Week 3 Recurrence Representation Review

**Owner:** Aahmad Sayeed  
**Role:** Recurrence Representation Lead

## Input

```text
64 × 11 chronological CAN sequence
```

## Output

```text
64 × 64 recurrence-style image
```

## Transformation

The compact signal combines:

- 35% normalised CAN ID;
- 10% normalised DLC;
- 45% mean normalised payload;
- 10% normalised timing.

Pairwise absolute distance is converted to similarity using an exponential transformation.

## Review Checks

- image shape is `64 × 64`;
- image values are finite and within `[0,1]`;
- labels and attack ratios are not used;
- one example is inspected for every class;
- images are generated after the protected split exists;
- information loss from payload averaging is documented.

## Week Boundary

CNN training is scheduled for Week 5.
