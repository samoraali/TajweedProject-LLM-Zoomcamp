from __future__ import annotations

from sentence_transformers import SentenceTransformer

from tajweed_ai_assistant.retrieval.rerank import rerank_results
from tajweed_ai_assistant.retrieval.search import (
    DEFAULT_KB,
    DEFAULT_MODEL,
    build_index,
    load_knowledge_base,
    search,
)

from .prompt import SYSTEM_PROMPT, build_rag_prompt
from .generator import generate_answer


def retrieve_context(
    query: str,
    records: list[dict],
    embeddings,
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[dict]:
    """Retrieve and rerank the most relevant knowledge-base chunks."""

    semantic_results = search(
        query,
        records,
        embeddings,
        model,
        top_k=5,
    )

    return rerank_results(
        query,
        semantic_results,
        top_k=top_k,
    )


def build_rag_request(
    query: str,
    records: list[dict],
    embeddings,
    model: SentenceTransformer,
    top_k: int = 3,
) -> dict:
    """Build everything needed for an LLM RAG request."""

    results = retrieve_context(
        query,
        records,
        embeddings,
        model,
        top_k=top_k,
    )

    user_prompt = build_rag_prompt(
        query,
        results,
    )

    return {
        "system_prompt": SYSTEM_PROMPT,
        "user_prompt": user_prompt,
        "results": results,
    }


def load_rag_resources(
    kb_path=DEFAULT_KB,
    model_name=DEFAULT_MODEL,
):
    """Load the knowledge base, embedding model, and passage embeddings."""

    records = load_knowledge_base(kb_path)

    model = SentenceTransformer(model_name)

    embeddings = build_index(
        records,
        model,
    )

    return records, model, embeddings

def answer_question(
    query: str,
    records: list[dict],
    embeddings,
    model: SentenceTransformer,
    top_k: int = 3,
) -> dict:
    """Retrieve context and generate a grounded answer."""

    request = build_rag_request(
        query,
        records,
        embeddings,
        model,
        top_k=top_k,
    )

    answer = generate_answer(
        query=query,
        user_prompt=request["user_prompt"],
    )

    return {
        "query": query,
        "answer": answer,
        "results": request["results"],
    }