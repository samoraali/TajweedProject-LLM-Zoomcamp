from pathlib import Path
from collections import Counter
import json
import unicodedata


PAGES_PATH = Path("data/processed/raw_pages.jsonl")

START_PAGE = 115
END_PAGE = 135


def is_arabic_letter(character):
    return (
        "\u0600" <= character <= "\u06FF"
        and character.isalpha()
    )


def count_suspicious_spaces(text):
    count = 0

    for i in range(1, len(text) - 1):
        if (
            text[i] == " "
            and is_arabic_letter(text[i - 1])
            and is_arabic_letter(text[i + 1])
        ):
            count += 1

    return count


def analyze_pages():
    total_characters = 0
    total_suspicious_spaces = 0

    with PAGES_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            page = json.loads(line)

            page_number = page["pdf_page"]

            if not START_PAGE <= page_number <= END_PAGE:
                continue

            text = page["text"]

            characters = len(text)
            suspicious_spaces = count_suspicious_spaces(text)

            total_characters += characters
            total_suspicious_spaces += suspicious_spaces

            print(
                f"Page {page_number:3} | "
                f"characters: {characters:5} | "
                f"suspicious spaces: {suspicious_spaces:4}"
            )

    print("\n" + "=" * 70)
    print("SAMPLE TOTAL")
    print("=" * 70)
    print(f"Pages:              {END_PAGE - START_PAGE + 1}")
    print(f"Characters:         {total_characters}")
    print(f"Suspicious spaces:  {total_suspicious_spaces}")


def main():
    analyze_pages()


if __name__ == "__main__":
    main()