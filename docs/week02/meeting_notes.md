# Week 2 Technical Meeting Notes

**Date:**  
**Chair:** Miftha Thahniyath  
**Attendees:** Amit Das, Aahmad Sayeed, Maheswari Kamireddy, Miftha Thahniyath, Nagireddy Nakka

## Topics Reviewed

1. HCRL file discovery.
2. DLC-aware parsing.
3. Normal and attack flags.
4. Source-level audit outputs.
5. EDA coverage.
6. Required metadata for later reporting.
7. Responsible-data rules.
8. Week 3 handover.

## Decisions

| Decision | Reason |
|---|---|
| Keep raw data outside GitHub | Files are large and should remain in Kaggle |
| Use chunked parsing | Multi-million-row files should not be loaded entirely into memory |
| Retain chronological order | Later LSTM modelling depends on temporal sequence |
| Do not train models in Week 2 | Weekly GitHub evidence must remain incremental |
| Move windowing and split to Week 3 | Prevents Week 2 from consuming later milestones |

## Actions

| Member | Action |
|---|---|
| Amit | Finalise parser and Week 2 notebook |
| Aahmad | Review EDA and recurrence requirements |
| Maheswari | Review sequence requirements |
| Miftha | Document reporting metadata |
| Nagireddy | Review responsible-data handling and limitations |
