# HANDOFF — AutoSPECTRA (AAI 55-710603)
*Updated 2026-06-18*

## 1. Where it stands
**Direction LOCKED: AutoSPECTRA — deep-learning intrusion detection for the car's CAN bus.** The repo is reframed and the baseline prototype runs end-to-end. Verified this session: `python src/can_ids.py --demo` generates CAN traffic with injected attacks, trains a classifier, reports per-class precision/recall/F1, and auto-writes an incident report. Swap in the HCRL Car-Hacking dataset for real numbers.

## 2. Why this won (the strategic call)
The SPECTRA EM side-channel idea was killed by two facts: its marquee live demo (over-the-air EM attack, "the room goes quiet") is the **highest-risk** thing you could pick and the live demo is worth **30%**, and it needs RF skills the group doesn't have. Also, **implementation is only 10%** of the grade. AutoSPECTRA keeps the embedded-security sophistication, runs on a **free public dataset (no hardware)**, covers all three module blocks (Computer Vision via CAN→image CNN, NLP via the report, plus the DL evaluation), and merges with your RSC fraud topic + NOMAD. Marks live in **Evaluation 30% + Pitch 30% + Ethics 20% = 80%** — build a modest model, then invest there. Full coverage map: `docs/PROJECT-PLAN.md`.

## 3. What's in the repo
`README.md`, `docs/PROJECT-PLAN.md` (locked scope + brief-coverage map), `PROPOSAL.md` (Parts A–F), `LITERATURE.md` (9 CAN-IDS citations), `EVALUATION.md` (30% plan), `ETHICS.md` (20%), `PITCH-OUTLINE.md` (30%), `src/can_ids.py` (runnable baseline), `requirements.txt`, `AI-USE-LOG.md`, `GEMINI-PROMPT.md`. The old RAG/LemonCheck version is in `_archive/rag-version/` (not deleted).

## 4. Blocked — needs a human
1. **Deadline: 18/08/2026 (confirmed from brief)** → email Royce for Week 11/12 slot confirmation (template §6).
2. **Group buy-in + roles** → pitch `docs/PROJECT-PLAN.md`; gives the SPECTRA proposer the CNN role.
3. **Repo not on GitHub** → push today (evidence rule; you're behind after the missed session).
4. **Real data** → download HCRL Car-Hacking, wire the loader, re-run for real metrics.
5. **Deep models** → baseline runs; the CNN-on-image + LSTM are the next build.

## 5. Next actions, in order
1. **Push to GitHub today:**
   ```bash
   cd project-repo
   git init && git add . && git commit -m "feat: AutoSPECTRA CAN-IDS baseline; docs: plan, lit, eval, ethics, pitch"
   gh repo create aai-autospectra --private --source=. --push
   ```
2. **Email Royce** to confirm the deadline (§6).
3. **Pitch `PROJECT-PLAN.md` to the group**, assign the three layers.
4. **Download Car-Hacking**, wire the loader, re-run eval → first real numbers (report Part D).
5. Train the CNN-on-image model; build the Streamlit demo.

## 6. Message templates
**To Royce Copley (Royce.Copley@shu.ac.uk):**
> Subject: AAI project — submission date + direction check
> Hi Royce, our group is focusing on deep-learning intrusion detection for the vehicle CAN bus (using the HCRL Car-Hacking dataset). Could you confirm the submission deadline and the Week 11/12 pitch slot? Thanks, Ad.

**To the group:**
> I've pushed our repo reframed around CAN-bus intrusion detection — same embedded-security + deep-learning idea, but on a free real dataset so the live demo actually works (no RF kit). It covers the CV block (CAN→image CNN), NLP (auto incident report) and a strong evaluation. Baseline already runs. Proposed layers: data+eval / CV model / sequence model + report. Repo: [link]. 10 mins to lock roles?

## 7. Run
```bash
pip install -r requirements.txt
python src/can_ids.py --demo
```
