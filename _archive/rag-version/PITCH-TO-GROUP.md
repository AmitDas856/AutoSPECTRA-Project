# Pitch to the group — sharpen our project into "LemonCheck"

> *Working name:* **LemonCheck** — an offline AI assistant that reads a used car's documents and flags the lemons. (Nod to Akerlof's "market for lemons," our economics hook.)

## The one-liner
Same offline-RAG system we already built, pointed at a real, vivid problem: **buying a dodgy second-hand car.** Feed it a car's service history, MOT records, and the seller's listing; it answers questions and **flags inconsistencies that signal fraud** (mileage that contradicts the service record, cleared fault codes, undeclared repairs) — all on a laptop, offline.

## Why this is a stronger project (not a restart)
- **Nothing is thrown away.** Same stack (local LLM + retrieval + grounding), same repo, same GitHub history. We only change the **corpus and the framing**. Zero lost evidence.
- **The live demo becomes memorable.** "Ask it about this car → it catches the rollback" beats "ask it about a PDF." The pitch is 30% of the grade and rewards a killer demo.
- **Ethics gets richer (20%):** consumer protection, the harm of false fraud accusations, fairness across sellers, privacy of buyers — far more to say than generic RAG ethics.
- **Concrete = higher marks.** The rubric rewards "independent insight" and a problem at "the forefront of the discipline." A specific, real-world fraud problem reads as exactly that.

## What changes vs what stays
| Stays (already done) | Changes (small) |
|---|---|
| Local RAG pipeline, prototype, eval harness | Demo corpus → car service histories, MOT/HMRC docs, listings |
| Evaluation metrics (recall@k, faithfulness) | Add a **fraud-flag** output + a few "inconsistency" test cases |
| Ethics structure | Re-angle to consumer protection / false-accusation harm |
| GitHub evidence + roles | Project name + problem framing |

## The demo (what tutors will see)
1. Load one car's documents.
2. Ask "what's the service history?" → grounded answer with sources.
3. Ask "is the mileage consistent?" → it cross-checks and **flags** the inconsistency.
4. Ask something not in the docs → it refuses (honesty).

## Suggested roles (3 people)
- **Retrieval + evaluation** (recall@k, the test set).
- **Generation + fraud-flag logic + UI** (the demo).
- **Data + ethics** (assemble the car-doc corpus, write the ethics/impact section).

## Copy-paste message for the group chat
> Idea to sharpen our offline-RAG project: keep everything we've built, but point it at **used-car buying** — feed it a car's service history + MOT + listing and have it answer questions *and flag fraud* (e.g. mileage that doesn't match the records). Same tech, same repo, way better live demo, and loads more to say on ethics. I've drafted a one-pager + updated the proposal. Worth 10 mins to discuss? I can demo the current prototype.

## Framing for Royce / tutors (continuity, not a pivot)
"We've focused our offline-RAG assistant onto a concrete domain — used-car fraud detection — to strengthen the live demo and the ethical evaluation. The architecture is unchanged from our Week-1 pitch; we've specialised the application." (This protects your continuous-engagement score: it's evolution, not a restart.)
