from pathlib import Path
from collections import Counter
import json
import unicodedata


PAGES_PATH = Path("data/processed/pages.jsonl")
TARGET_PAGE = 120


def load_page(page_number):
    with PAGES_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            page = json.loads(line)

            if page["pdf_page"] == page_number:
                return page["text"]

    return None


def analyze_characters(text):
    counter = Counter(text)

    print(f"Text length: {len(text)}")
    print(f"Unique characters: {len(counter)}")
    print()

    print("Most common characters:")
    print("-" * 60)

    for character, count in counter.most_common(30):
        if character.isspace():
            display = "[WHITESPACE]"
            name = "WHITESPACE"
        else:
            display = repr(character)
            name = unicodedata.name(character, "UNKNOWN")

        print(
            f"{display:15} "
            f"{count:5} "
            f"U+{ord(character):04X} "
            f"{name}"
        )


if __name__ == "__main__":
    text = load_page(TARGET_PAGE)

    if text is None:
        raise ValueError(f"Page {TARGET_PAGE} not found")

    analyze_characters(text)