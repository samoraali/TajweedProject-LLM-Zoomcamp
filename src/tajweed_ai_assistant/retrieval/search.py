from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


DEFAULT_KB = Path("data/processed/knowledge_base.jsonl")
DEFAULT_MODEL = "intfloat/multilingual-e5-small"


def load_knowledge_base(path: Path) -> list[dict]:
    """Load Tajweed chunks from JSONL."""
    records = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    """L2-normalize embeddings for cosine similarity."""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / np.clip(norms, 1e-12, None)


def build_index(
    records: list[dict],
    model: SentenceTransformer,
) -> np.ndarray:
    """Create normalized passage embeddings."""
    passages = [
        f"passage: {record['text']}"
        for record in records
    ]

    embeddings = model.encode(
        passages,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    return normalize_embeddings(embeddings)


def search(
    query: str,
    records: list[dict],
    passage_embeddings: np.ndarray,
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[dict]:
    """Return the most relevant Tajweed chunks."""
    query_embedding = model.encode(
        [f"query: {query}"],
        convert_to_numpy=True,
    )

    query_embedding = normalize_embeddings(query_embedding)[0]

    scores = passage_embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        record = records[index].copy()
        record["score"] = float(scores[index])
        results.append(record)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Semantic search over the Tajweed knowledge base."
    )

    parser.add_argument(
        "query",
        help="Arabic question or search query",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--kb",
        type=Path,
        default=DEFAULT_KB,
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
    )

    args = parser.parse_args()

    print("Loading knowledge base...")
    records = load_knowledge_base(args.kb)

    print(f"Loaded {len(records)} chunks.")

    print(f"Loading embedding model: {args.model}")
    model = SentenceTransformer(args.model)

    print("Building embeddings...")
    embeddings = build_index(records, model)

    print(f"\nQuery: {args.query}")
    print("=" * 70)

    results = search(
        args.query,
        records,
        embeddings,
        model,
        top_k=args.top_k,
    )

    for rank, result in enumerate(results, start=1):
        print(
            f"\n#{rank} | "
            f"score={result['score']:.4f} | "
            f"page={result['pdf_page']} | "
            f"topic={result['topic']}"
        )

        print("-" * 70)
        print(result["text"])


if __name__ == "__main__":
    main()