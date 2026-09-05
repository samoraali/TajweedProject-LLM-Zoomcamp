from tajweed_ai_assistant.retrieval.search import (
    DEFAULT_KB,
    DEFAULT_MODEL,
    build_index,
    load_knowledge_base,
    search,
)


TEST_CASES = [
    # ------------------------------------------------------------------
    # الإظهار الحلقي
    # ------------------------------------------------------------------
    {
        "query": "ما هو الإظهار الحلقي؟",
        "expected_pages": {120, 121, 122},
        "expected_topic": "الإظهار الحلقي",
    },
    {
        "query": "ما المقصود بالإظهار الحلقي؟",
        "expected_pages": {120},
        "expected_topic": "الإظهار الحلقي",
    },
    {
        "query": "ما هي حروف الإظهار الحلقي؟",
        "expected_pages": {120},
        "expected_topic": "الإظهار الحلقي",
    },
    {
        "query": "متى يكون الإظهار الحلقي؟",
        "expected_pages": {120, 121},
        "expected_topic": "الإظهار الحلقي",
    },
    {
        "query": "كيف يكون النطق في الإظهار الحلقي؟",
        "expected_pages": {120, 122},
        "expected_topic": "الإظهار الحلقي",
    },

    # ------------------------------------------------------------------
    # الإدغام
    # ------------------------------------------------------------------
    {
        "query": "ما هو الإدغام؟",
        "expected_pages": {123, 124, 125, 126, 127, 128},
        "expected_topic": "الإدغام",
    },
    {
        "query": "ما المقصود بالإدغام؟",
        "expected_pages": {123, 125},
        "expected_topic": "الإدغام",
    },
    {
        "query": "ما هي حروف الإدغام؟",
        "expected_pages": {123, 125},
        "expected_topic": "الإدغام",
    },
    {
        "query": "ما أقسام الإدغام؟",
        "expected_pages": {124, 125, 126, 127},
        "expected_topic": "الإدغام",
    },
    {
        "query": "ما الفرق بين الإدغام الكامل والإدغام الناقص؟",
        "expected_pages": {125},
        "expected_topic": "الإدغام",
    },
    {
        "query": "متى يحدث الإدغام مع النون الساكنة والتنوين؟",
        "expected_pages": {123, 125},
        "expected_topic": "الإدغام",
    },
    {
        "query": "كيف يتم الإدغام؟",
        "expected_pages": {123, 125},
        "expected_topic": "الإدغام",
    },

    # ------------------------------------------------------------------
    # الإقلاب
    # ------------------------------------------------------------------
    {
        "query": "ما هو الإقلاب؟",
        "expected_pages": {129, 130, 131},
        "expected_topic": "الإقلاب",
    },
    {
        "query": "ما المقصود بالإقلاب؟",
        "expected_pages": {129},
        "expected_topic": "الإقلاب",
    },
    {
        "query": "ما هو حرف الإقلاب؟",
        "expected_pages": {129},
        "expected_topic": "الإقلاب",
    },
    {
        "query": "ما هي حروف الإقلاب؟",
        "expected_pages": {129},
        "expected_topic": "الإقلاب",
    },
    {
        "query": "كيف يتم أداء الإقلاب؟",
        "expected_pages": {129, 130, 131},
        "expected_topic": "الإقلاب",
    },
    {
        "query": "لماذا اختيرت الميم في حكم الإقلاب؟",
        "expected_pages": {130},
        "expected_topic": "الإقلاب",
    },

    # ------------------------------------------------------------------
    # الإخفاء الحقيقي
    # ------------------------------------------------------------------
    {
        "query": "ما هو الإخفاء الحقيقي؟",
        "expected_pages": {132, 133, 134, 135},
        "expected_topic": "الإخفاء الحقيقي",
    },
    {
        "query": "ما المقصود بالإخفاء الحقيقي؟",
        "expected_pages": {132},
        "expected_topic": "الإخفاء الحقيقي",
    },
    {
        "query": "ما هي حروف الإخفاء الحقيقي؟",
        "expected_pages": {132},
        "expected_topic": "الإخفاء الحقيقي",
    },
    {
        "query": "كم عدد حروف الإخفاء الحقيقي؟",
        "expected_pages": {132},
        "expected_topic": "الإخفاء الحقيقي",
    },
    {
        "query": "كيف تكون الغنة في الإخفاء الحقيقي؟",
        "expected_pages": {133, 134, 135},
        "expected_topic": "الإخفاء الحقيقي",
    },
    {
        "query": "ما مراتب الإخفاء الحقيقي؟",
        "expected_pages": {134},
        "expected_topic": "الإخفاء الحقيقي",
    },

    # ------------------------------------------------------------------
    # Cross-topic / comparative question
    # ------------------------------------------------------------------
    {
        "query": "ما الفرق بين الإظهار والإدغام والإقلاب والإخفاء؟",
        "expected_pages": {115, 120, 123, 129, 132},
        "expected_topic": "فهرس / نظرة عامة",
    },
]


def hit_at(results, k, expected_pages):
    """Return True if any top-k result belongs to an expected page."""
    return any(
        result["pdf_page"] in expected_pages
        for result in results[:k]
    )


def topic_hit_at(results, k, expected_topic):
    """Return True if any top-k result has the expected topic."""
    return any(
        result["topic"] == expected_topic
        for result in results[:k]
    )


def main():
    print("Loading knowledge base...")
    records = load_knowledge_base(DEFAULT_KB)

    print(f"Records: {len(records)}")
    print(f"Loading model: {DEFAULT_MODEL}")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(DEFAULT_MODEL)

    print("Building retrieval index...")
    embeddings = build_index(records, model)

    print("\n" + "=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    results_by_query = []

    for i, case in enumerate(TEST_CASES, start=1):
        results = search(
            case["query"],
            records,
            embeddings,
            model,
            top_k=5,
        )

        hit1 = hit_at(results, 1, case["expected_pages"])
        hit3 = hit_at(results, 3, case["expected_pages"])
        hit5 = hit_at(results, 5, case["expected_pages"])

        topic1 = topic_hit_at(
            results,
            1,
            case["expected_topic"],
        )

        topic3 = topic_hit_at(
            results,
            3,
            case["expected_topic"],
        )

        results_by_query.append(
            {
                "hit1": hit1,
                "hit3": hit3,
                "hit5": hit5,
                "topic1": topic1,
                "topic3": topic3,
            }
        )

        print(f"\n{i}. {case['query']}")
        print(f"   Expected topic: {case['expected_topic']}")
        print(
            f"   Expected pages: "
            f"{sorted(case['expected_pages'])}"
        )

        print(
            f"   Hit@1={hit1} | "
            f"Hit@3={hit3} | "
            f"Hit@5={hit5}"
        )

        print(
            f"   Topic@1={topic1} | "
            f"Topic@3={topic3}"
        )

        print("   Top results:")

        for rank, result in enumerate(results[:3], start=1):
            text_preview = (
                result["text"]
                .replace("\n", " ")
                .strip()
            )

            if len(text_preview) > 120:
                text_preview = text_preview[:120] + "..."

            print(
                f"      #{rank} "
                f"score={result['score']:.4f} "
                f"page={result['pdf_page']} "
                f"topic={result['topic']}"
            )

            print(f"         {text_preview}")

    total = len(results_by_query)

    hit1_score = (
        sum(r["hit1"] for r in results_by_query) / total
    )

    hit3_score = (
        sum(r["hit3"] for r in results_by_query) / total
    )

    hit5_score = (
        sum(r["hit5"] for r in results_by_query) / total
    )

    topic1_score = (
        sum(r["topic1"] for r in results_by_query) / total
    )

    topic3_score = (
        sum(r["topic3"] for r in results_by_query) / total
    )

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"Test queries: {total}")
    print(f"Hit@1:        {hit1_score:.1%}")
    print(f"Hit@3:        {hit3_score:.1%}")
    print(f"Hit@5:        {hit5_score:.1%}")
    print(f"Topic@1:      {topic1_score:.1%}")
    print(f"Topic@3:      {topic3_score:.1%}")


if __name__ == "__main__":
    main()