#!/usr/bin/env python3
"""
Offline RAG Assistant - document-aware prototype (AAI group project).

Pipeline:  documents -> chunk -> embed (local) -> retrieve top-k -> local LLM -> grounded answer + sources
Everything runs LOCALLY via Ollama (http://localhost:11434). No cloud, no API keys.

This version ingests REAL documents from a folder (.md/.txt, and .pdf if `pypdf`
is installed), so it is demoable for the Week 11/12 pitch. It degrades gracefully:
if Ollama is not running it falls back to keyword retrieval and prints a clear
message, so the shape of the system is always visible (safe to commit + demo-plan).

Quick start:
    ollama serve &                 # one terminal
    ollama pull llama3.2:3b        # generator
    ollama pull nomic-embed-text   # embeddings
    pip install -r requirements.txt
    python src/rag_prototype.py --corpus ../md --ask "what does the assessment brief require?"
"""
from __future__ import annotations

import argparse
import glob
import math
import os
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import requests
except ImportError:  # keep importable with a clear message
    requests = None  # type: ignore

try:
    import numpy as np  # optional: faster cosine if present
except ImportError:
    np = None  # type: ignore

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
GEN_MODEL = os.environ.get("RAG_GEN_MODEL", "llama3.2:3b")
EMBED_MODEL = os.environ.get("RAG_EMBED_MODEL", "nomic-embed-text")

# Fallback corpus used only if no documents are found, so the script always runs.
TOY_CORPUS = [
    "Retrieval-Augmented Generation (RAG) grounds a language model's answer in retrieved documents, reducing hallucination.",
    "Embeddings turn text into vectors so semantically similar passages sit close together; similarity is cosine distance.",
    "Running the LLM and the embedding model locally via Ollama keeps all data on-device, which matters for privacy and offline use.",
    "RAG evaluation separates retrieval quality (recall@k, context precision) from answer quality (faithfulness, answer relevancy).",
]


@dataclass
class Chunk:
    """A retrievable unit of text plus where it came from (for citations)."""
    text: str
    source: str
    embedding: Optional[list[float]] = None


# --------------------------------------------------------------------------- #
# 1. Load + chunk documents
# --------------------------------------------------------------------------- #
def _read_file(path: str) -> str:
    if path.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
            return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
        except Exception:
            return ""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except Exception:
        return ""


def load_chunks(corpus_dir: Optional[str], size: int = 800, overlap: int = 120) -> list[Chunk]:
    """Read .md/.txt/.pdf from corpus_dir and split into overlapping char chunks."""
    if not corpus_dir or not os.path.isdir(corpus_dir):
        return [Chunk(text=t, source="toy_corpus") for t in TOY_CORPUS]
    paths: list[str] = []
    for ext in ("*.md", "*.txt", "*.pdf"):
        paths.extend(glob.glob(os.path.join(corpus_dir, "**", ext), recursive=True))
    chunks: list[Chunk] = []
    for path in sorted(paths):
        text = " ".join(_read_file(path).split())
        name = os.path.basename(path)
        step = max(1, size - overlap)
        for start in range(0, len(text), step):
            piece = text[start:start + size]
            if len(piece) > 40:  # skip tiny tail fragments
                chunks.append(Chunk(text=piece, source=name))
    return chunks or [Chunk(text=t, source="toy_corpus") for t in TOY_CORPUS]


# --------------------------------------------------------------------------- #
# 2. Embed (local) + retrieve
# --------------------------------------------------------------------------- #
def embed(text: str) -> Optional[list[float]]:
    """Local embedding via Ollama. Returns a vector, or None if the service is down."""
    if requests is None:
        return None
    try:
        r = requests.post(f"{OLLAMA}/api/embeddings",
                          json={"model": EMBED_MODEL, "prompt": text}, timeout=30)
        return r.json().get("embedding")
    except Exception:
        return None


def cosine(a: list[float], b: list[float]) -> float:
    if np is not None:
        va, vb = np.asarray(a), np.asarray(b)
        return float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)


def keyword_score(question: str, text: str) -> int:
    """Cheap lexical overlap, used when embeddings are unavailable so the demo still runs."""
    q = set(w.lower().strip(".,?!") for w in question.split())
    return sum(w in text.lower() for w in q)


def retrieve(question: str, chunks: list[Chunk], k: int = 4) -> tuple[list[Chunk], str]:
    """Return the top-k chunks and the mode used ('embeddings' or 'keyword-fallback')."""
    qv = embed(question)
    if qv is None:
        ranked = sorted(chunks, key=lambda c: keyword_score(question, c.text), reverse=True)
        return ranked[:k], "keyword-fallback"
    for c in chunks:
        if c.embedding is None:
            c.embedding = embed(c.text)
    scored = [(cosine(qv, c.embedding), c) for c in chunks if c.embedding]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [c for _, c in scored[:k]], "embeddings"


# --------------------------------------------------------------------------- #
# 3. Generate (grounded, with refusal)
# --------------------------------------------------------------------------- #
def generate(question: str, context: list[Chunk]) -> str:
    """Ask the local LLM to answer using ONLY the retrieved context, or refuse."""
    numbered = "\n".join(f"[{i}] ({c.source}) {c.text}" for i, c in enumerate(context, 1))
    prompt = (
        "You are a careful assistant. Answer the question using ONLY the context below. "
        "Cite the [number] of each context passage you use. "
        "If the context does not contain the answer, reply exactly: "
        "'I cannot answer that from the provided documents.'\n\n"
        f"Context:\n{numbered}\n\nQuestion: {question}\nAnswer:"
    )
    if requests is None:
        return "[requests not installed - run: pip install -r requirements.txt]"
    try:
        r = requests.post(f"{OLLAMA}/api/generate",
                          json={"model": GEN_MODEL, "prompt": prompt, "stream": False}, timeout=180)
        return r.json().get("response", "").strip()
    except Exception:
        return (f"[Ollama not reachable on {OLLAMA} - start it with `ollama serve` and "
                f"`ollama pull {GEN_MODEL}`. Retrieved context is shown above; the wiring is correct.]")


# --------------------------------------------------------------------------- #
# 4. CLI
# --------------------------------------------------------------------------- #
def answer(question: str, corpus_dir: Optional[str], k: int = 4) -> None:
    chunks = load_chunks(corpus_dir)
    ctx, mode = retrieve(question, chunks, k)
    print(f"\n[corpus: {len(chunks)} chunks | retrieval: {mode} | top-{k}]")
    print("\n=== retrieved sources ===")
    for i, c in enumerate(ctx, 1):
        preview = (c.text[:140] + "...") if len(c.text) > 140 else c.text
        print(f"  [{i}] ({c.source}) {preview}")
    print("\n=== grounded answer ===")
    print(generate(question, ctx))


def main() -> None:
    ap = argparse.ArgumentParser(description="Offline RAG prototype (local Ollama).")
    ap.add_argument("--ask", required=True, help="your question")
    ap.add_argument("--corpus", default=None,
                    help="folder of .md/.txt/.pdf documents (default: built-in toy corpus)")
    ap.add_argument("-k", type=int, default=4, help="passages to retrieve")
    args = ap.parse_args()
    answer(args.ask, args.corpus, args.k)


if __name__ == "__main__":
    main()
