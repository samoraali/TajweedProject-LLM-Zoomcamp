from __future__ import annotations

from tajweed_ai_assistant.rag.pipeline import (
    answer_question,
    load_rag_resources,
)


def print_sources(results: list[dict]) -> None:
    print("\nالمصادر:")
    for result in results:
        page = result.get("pdf_page", result.get("page", "غير معروف"))
        topic = result.get("topic", "غير معروف")
        print(f"- الصفحة {page} — {topic}")


def main() -> None:
    print("Tajweed AI Assistant")
    print("اكتب سؤالك بالعربية. اكتب 'خروج' لإنهاء المحادثة.")
    print()

    print("Loading RAG resources...")
    records, model, embeddings = load_rag_resources()
    print("Resources loaded.")
    print()

    while True:
        try:
            query = input("السؤال: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nتم إنهاء المحادثة.")
            break

        if not query:
            continue

        if query.lower() in {"خروج", "exit", "quit"}:
            print("تم إنهاء المحادثة.")
            break

        result = answer_question(
            query,
            records,
            embeddings,
            model,
        )

        print("\nالإجابة:")
        print(result["answer"])
        print_sources(result["results"])
        print()


if __name__ == "__main__":
    main()
