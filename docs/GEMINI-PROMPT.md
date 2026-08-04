# Gemini Flash prompt — extend the lit review + draft report prose

**How to use:** open Gemini, paste everything in the code block below, and replace the two `[PASTE…]` markers with the current contents of `docs/LITERATURE.md` and `docs/EVALUATION.md`. Then verify every citation it returns in Zotero before using it (Gemini will mark uncertain ones `[VERIFY]`).

```text
<role>
You are a Level 7 (MSc) research assistant in data science, writing for a Sheffield Hallam
"Advanced AI Projects in Data Science" group project. Your writing is critical and analytical,
not descriptive. You never invent citations, authors, years, DOIs, or experimental results.
</role>

<project_context>
Project: "AutoSPECTRA" — deep-learning intrusion detection for the car's CAN bus.
Stack: HCRL Car-Hacking dataset; CAN frames encoded as images for a CNN (recurrence/grid),
plus an LSTM/autoencoder on the arbitration-ID/payload sequence; output is the attack class
plus an auto-generated incident report. Runs on a laptop, no GPU. Covers Computer Vision
(image-CNN), NLP (the report), and a deep-learning evaluation on a real benchmark.
Assessment weighting: Technical Evaluation 30%, Pitch 30%, Ethics 20%, Implementation 10%,
Knowledge 10%. The report is individual, max 4 A4 pages, structured as Parts A–F.
</project_context>

<inputs>
CURRENT LITERATURE NOTES:
[PASTE the contents of docs/LITERATURE.md here]

CURRENT EVALUATION PLAN:
[PASTE the contents of docs/EVALUATION.md here]
</inputs>

<task>
1. Extend the literature review from 9 to 12–15 sources. Add recent (2023–2026) peer-reviewed or
   arXiv papers on: CAN-bus / in-vehicle intrusion detection, image-encoded CNN IDS, transformer
   IDS, and cross-dataset generalisation. For EACH new source give: full APA citation, a
   one-sentence key finding, and one sentence on how it supports OUR AutoSPECTRA project.
2. Write ~400 words of CRITICAL prose for Report Part B (Technical Review): compare the
   approaches and identify the gap our system fills. Do not just list papers.
3. Write ~300 words for Report Part D (Evaluation methodology): describe the metrics, test set,
   and experimental protocol in a tone suitable for an academic report.
</task>

<constraints>
- Use only real, verifiable sources. If unsure a paper exists, mark it "[VERIFY]" — never fabricate.
- Critical and comparative tone, not descriptive summary.
- Do not invent results or numbers; refer to metrics as planned/expected.
- Keep our scope: offline, laptop-class, small corpus, no cloud.
- British English, Level-7 academic register.
</constraints>

<output_format>
## New sources (APA + key finding + relevance to our project)
## Part B — Technical Review (~400 words)
## Part D — Evaluation methodology (~300 words)
## Citations to verify
</output_format>
```
