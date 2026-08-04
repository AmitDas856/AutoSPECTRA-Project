# AI-Use Log (integrity & ethics)

> Declare AI assistance honestly — it strengthens the Ethics/Responsible-Research grade (20%) rather than risking it. One row per meaningful use. Write the report and code understanding in your own words.

| Date | Tool | What it was asked | How the output was used |
|---|---|---|---|
| 2026-06-05 | Claude (Cowork) | Scaffold this repo (README, board, proposal skeleton, prototype stub) | Starting structure; team writes the actual content, lit review, and report |
| 2026-06-18 | Claude (Cowork) | Add technical-review citations, evaluation plan, ethics analysis, pitch outline; upgrade prototype to ingest real documents + add eval harness | Shared scaffolding and sourced facts; each member writes their own report prose and verifies citations in Zotero |
| 2026-06-18 | Claude (Cowork) | Re-focus project onto CAN-bus intrusion detection (AutoSPECTRA); brief-coverage map, reframed proposal, runnable CAN-IDS prototype + literature | Shared project scaffolding; team writes report prose, trains the real models, and verifies citations |

| 2026-06-29 | Claude (Sonnet) | Set up GitHub repo, create issues/board, fix deadline dates, complete frames_to_image encoder TODO | Repo setup and issue creation; I wrote the encoder, understand the normalisation and channel reshape for the viva |
| 2026-06-29/30 | Claude (Sonnet) | Scaffold HCRL loader + time-ordered split, evaluation harness, baseline runner; debug Windows/memory issues | Amit reviewed every function and re-ran everything; found + fixed the missing-test-classes problem with the per-file split (documented in results_week6.md) |
| 2026-06-30 | Claude (Fable) | Add detection-latency metric + RandomForest comparison to the harness; wire TinyCNN to the real split with windowing (train_cnn.py); clean up stale scripts | Code reviewed line-by-line by Amit (eval) and Ad (CNN wiring); each explains their slice in the viva. All numbers are real runs on the HCRL test tail |
| 2026-07-02 | Claude (Fable) | Make window size a CLI arg in train_cnn.py and run the WINDOW=16/64 ablation | 3-line change reviewed by Ad; ablation numbers are real runs through the shared harness on the same split |
| 2026-07-02 | Claude (Fable) | Add recurrence-plot encoder + grid-vs-recurrence encoding ablation; build the terminal fallback demo (src/demo.py) | Ad reviewed and ran both; the recurrence result (grid wins, 0.9857 vs 0.8452) and the demo detections are real runs. Ad explains the encoder and demo in the viva |
| 2026-07-08 | Claude (Fable) | While the other three members were unreachable, build their slices (LSTM sequence model, incident-report generator, Streamlit dashboard) and scaffold the ethics/literature sections; commit them under Ad's and Amit's names | **Corrected on 2026-07-28 — see below.** This code was AI-written and had not been read or run by the members it was committed under. |
| 2026-07-28 | Claude (Opus) | Review the repo against the AITS-2 rules and correct the above | The 2026-07-08 commits attributed AI-written work to people who had not reviewed it and could not have defended it in the viva. They were reverted (commit `88ab63c`) rather than rewritten, so the correction stays visible in the history. The code is staged in `_inbox/` for each owner to bring in, understand, and commit themselves. No AI-written code now sits in the repo under a name that has not reviewed it. |

<!-- Add rows as you use Gemini/Antigravity/Copilot for lit review, code help, or drafting. -->

> **Needs Ad's confirmation before submission:** the rows above dated 2026-06-29 to 2026-07-02 state that code was "reviewed line-by-line" or "reviewed and ran" by Ad or Amit. Each person should check that this is actually true of their own rows and correct any that overstate what they did. A declaration that overstates human review is the thing that breaks AITS-2 — not the AI use itself.
