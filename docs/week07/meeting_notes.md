# Week 7 Technical Meeting Notes

**Chair:** Miftha Thahniyath  
**Attendees:** Amit Das, Aahmad Sayeed, Maheswari Kamireddy, Miftha Thahniyath, Nagireddy Nakka

## Decisions

1. Fusion weights are selected using validation macro-F1.
2. Temperature is selected using validation log loss.
3. Test data is excluded from both selection processes.
4. Fusion is evaluated even if it does not beat Random Forest.
5. Calibration is judged by ECE/log loss rather than macro-F1 alone.
6. Detection latency is described as a window-based upper bound.
7. Feature ablation is executed in Week 7.
8. 32/64/128 window ablation is exported as a separate-run plan.
9. Incident reporting and Flask remain Week 8 tasks.
