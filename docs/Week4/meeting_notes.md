# Week 4 Technical Meeting Notes

**Date:**  
**Chair:** Miftha Thahniyath  
**Attendees:** Amit Das, Aahmad Sayeed, Maheswari Kamireddy, Miftha Thahniyath, Nagireddy Nakka

## Topics

1. Protected Week 3 test set.
2. Four classical baselines.
3. Macro-F1 as primary comparison metric.
4. Per-class error analysis.
5. FPR/FNR safety interpretation.
6. ROC, PR and reliability plots.
7. Inference cost and model size.
8. Image ZIP and GitHub evidence.
9. Week 5 CNN handover.

## Decisions

| Decision | Reason |
|---|---|
| Use the same Week 3 split for every model | Enables fair comparison |
| Train four tabular baselines | Establishes simple reference models |
| Save all major plots automatically | Reproducible evidence is stronger than screenshots |
| Keep model binaries outside normal Git commits | Avoid unnecessary repository growth |
| Use macro-F1 as primary metric | Equal importance for all five classes |
| Move CNN training to Week 5 | Preserve incremental development evidence |

## Actions

| Member | Action |
|---|---|
| Amit | Train baselines and maintain evaluation harness |
| Aahmad | Review saved evaluation plots |
| Maheswari | Compare model quality and efficiency |
| Miftha | Verify artifact ZIP and GitHub evidence |
| Nagireddy | Review safety implications and limitations |
