from pathlib import Path
import json


PAGES_PATH = Path("data/processed/raw_pages.jsonl")

START_PAGE = 115
END_PAGE = 135


def is_arabic_letter(character):
    return (
        "\u0600" <= character <= "\u06FF"
        and character.isalpha()
    )


def show_examples(text, limit=20):
    examples = []

    for i in range(1, len(text) - 1):
        if (
            text[i] == " "
            and is_arabic_letter(text[i - 1])
            and is_arabic_letter(text[i + 1])
        ):
            start = max(0, i - 15)
            end = min(len(text), i + 16)

            example = text[start:end].replace("\n", " ")
            examples.append(example)

            if len(examples) >= limit:
                break

    return examples


def main():
    with PAGES_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            page = json.loads(line)
            page_number = page["pdf_page"]

            if not START_PAGE <= page_number <= END_PAGE:
                continue

            examples = show_examples(page["text"])

            print("\n" + "=" * 80)
            print(f"PDF PAGE: {page_number}")
            print("=" * 80)

            for example in examples:
                print(example)


if __name__ == "__main__":
    main()