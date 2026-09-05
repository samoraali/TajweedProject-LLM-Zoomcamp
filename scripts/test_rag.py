from tajweed_ai_assistant.rag.pipeline import (
    answer_question,
    load_rag_resources,
)


def main():
    print("Loading RAG resources...")

    records, model, embeddings = load_rag_resources()

    print("Resources loaded.")
    print()

    query = "ما هو الإظهار الحلقي؟"

    print(f"Question: {query}")
    print()

    result = answer_question(
        query,
        records,
        embeddings,
        model,
    )

    print("ANSWER:")
    print(result["answer"])
    print()

    print("SOURCES:")

    for source in result["results"]:
        print(
            f"- page={source['pdf_page']} "
            f"topic={source['topic']}"
        )


if __name__ == "__main__":
    main()