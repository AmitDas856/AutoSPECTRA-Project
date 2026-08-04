#!/usr/bin/env python3
"""
Evaluation harness for the Offline RAG Assistant  (Report Part D - 30%).

Computes RETRIEVAL metrics over a labelled Q/A set:
  - recall@k : is the ground-truth source document among the top-k retrieved?
  - mean retrieval latency

It runs WITHOUT Ollama (using the keyword-fallback retriever) so you always get
numbers for the report; with Ollama running it uses real embeddings and the
numbers improve. Answer-quality metrics (faithfulness, answer relevancy) are
added on top with the `ragas` library - see docs/EVALUATION.md.

    python eval/run_eval.py --corpus ../md --qa eval/qa_set.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

# import the pipeline from ../src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import rag_prototype as rag  # noqa: E402


def load_qa(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def recall_at_k(corpus_dir: str, qa: list[dict], ks=(1, 3, 5)) -> None:
    chunks = rag.load_chunks(corpus_dir)
    answerable = [r for r in qa if r.get("source_doc")]
    maxk = max(ks)
    hits = {k: 0 for k in ks}
    latencies: list[float] = []

    for row in answerable:
        t0 = time.time()
        ctx, mode = rag.retrieve(row["q"], chunks, k=maxk)
        latencies.append(time.time() - t0)
        retrieved_sources = [c.source for c in ctx]
        for k in ks:
            if row["source_doc"] in retrieved_sources[:k]:
                hits[k] += 1

    n = max(1, len(answerable))
    print(f"\nCorpus: {len(chunks)} chunks | retrieval mode: {mode} | answerable Qs: {len(answerable)}")
    print("\n=== Retrieval recall@k ===")
    for k in ks:
        print(f"  recall@{k}: {hits[k]}/{n} = {hits[k]/n:.0%}")
    print(f"\nMean retrieval latency: {sum(latencies)/len(latencies):.3f}s")
    print("\n(Unanswerable questions in the set test refusal behaviour - check the")
    print(" generator says 'I cannot answer that from the provided documents'.)")


def main() -> None:
    ap = argparse.ArgumentParser(description="RAG retrieval evaluation")
    ap.add_argument("--corpus", default="../md", help="folder of source documents")
    ap.add_argument("--qa", default="eval/qa_set.jsonl", help="labelled Q/A set (jsonl)")
    args = ap.parse_args()
    recall_at_k(args.corpus, load_qa(args.qa))


if __name__ == "__main__":
    main()
