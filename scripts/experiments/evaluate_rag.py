from __future__ import annotations

from tajweed_ai_assistant.rag.pipeline import (
    answer_question,
    load_rag_resources,
)


TEST_QUESTIONS = [
    "ما هو الإظهار الحلقي؟",
    "ما هي حروف الإظهار الحلقي؟",
    "ما الفرق بين الإدغام الكامل والإدغام الناقص؟",
    "ما هو حرف الإقلاب؟",
    "كم عدد حروف الإخفاء الحقيقي؟",
]


def main() -> None:
    print("Loading RAG resources...")
    records, model, embeddings = load_rag_resources()
    print("Resources loaded.")
    print()

    for number, query in enumerate(TEST_QUESTIONS, start=1):
        print("=" * 70)
        print(f"السؤال {number}: {query}")

        result = answer_question(
            query,
            records,
            embeddings,
            model,
        )

        print("\nالإجابة:")
        print(result["answer"])

        print("\nالمصادر:")
        for source in result["results"]:
            page = source.get("pdf_page", source.get("page", "غير معروف"))
            topic = source.get("topic", "غير معروف")
            print(f"- الصفحة {page} — {topic}")

        print()


if __name__ == "__main__":
    main()
