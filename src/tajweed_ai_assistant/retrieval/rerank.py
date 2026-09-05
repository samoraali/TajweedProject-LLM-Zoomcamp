from __future__ import annotations

import re


TOPIC_NAMES = [
    "أحكام النون الساكنة والتنوين",
    "الإظهار الحلقي",
    "الإدغام",
    "الإقلاب",
    "الإخفاء الحقيقي",
]


STOPWORDS = {
    "ما",
    "هو",
    "هي",
    "من",
    "في",
    "مع",
    "عن",
    "إلى",
    "على",
    "ما",
    "كيف",
    "متى",
    "لماذا",
    "هل",
    "يكون",
    "يتم",
    "يحدث",
    "المقصود",
    "ماهي",
    "هي",
}


def normalize_arabic(text: str) -> str:
    """Normalize common Arabic spelling variations for matching."""
    text = text.lower()

    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)

    text = text.replace("أ", "ا")
    text = text.replace("إ", "ا")
    text = text.replace("آ", "ا")
    text = text.replace("ى", "ي")

    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text: str) -> list[str]:
    """Return meaningful normalized Arabic tokens."""
    normalized = normalize_arabic(text)

    return [
        token
        for token in normalized.split()
        if token not in STOPWORDS and len(token) > 1
    ]


def detect_topics(query: str) -> list[str]:
    """Detect all known Tajweed topics mentioned in the query."""
    normalized_query = normalize_arabic(query)

    return [
        topic
        for topic in TOPIC_NAMES
        if normalize_arabic(topic) in normalized_query
    ]


def lexical_score(query: str, result: dict) -> float:
    """Measure overlap between query terms and a retrieved chunk."""
    query_tokens = set(tokenize(query))

    if not query_tokens:
        return 0.0

    text_tokens = set(tokenize(result.get("text", "")))
    keyword_tokens = set(
        tokenize(" ".join(result.get("keywords", [])))
    )

    matched = query_tokens & (text_tokens | keyword_tokens)

    return len(matched) / len(query_tokens)


def rerank_results(
    query: str,
    results: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """
    Rerank semantic-search results using lightweight metadata
    and lexical relevance signals.
    """
    detected_topics = detect_topics(query)

    reranked = []

    for result in results:
        semantic_score = result["score"]

        lexical = lexical_score(query, result)

        topic_bonus = 0.0

        if len(detected_topics) == 1:
            if result.get("topic") == detected_topics[0]:
                topic_bonus = 0.08

        elif len(detected_topics) >= 2:
            if result.get("topic") == "فهرس / نظرة عامة":
                topic_bonus = 0.08

        final_score = (
            semantic_score
            + (0.05 * lexical)
            + topic_bonus
        )

        updated = result.copy()
        updated["semantic_score"] = semantic_score
        updated["lexical_score"] = lexical
        updated["rerank_score"] = final_score

        reranked.append(updated)

    reranked.sort(
        key=lambda result: result["rerank_score"],
        reverse=True,
    )

    return reranked[:top_k]