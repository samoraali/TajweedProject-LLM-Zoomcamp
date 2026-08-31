from pathlib import Path
import json


PAGES_PATH = Path("data/processed/pages.jsonl")

START_PAGE = 115
END_PAGE = 135


def is_arabic_letter(character):
    return (
        "\u0600" <= character <= "\u06FF"
        and character.isalpha()
    )


def analyze_spacing():
    with PAGES_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            page = json.loads(line)
            page_number = page["pdf_page"]

            if not START_PAGE <= page_number <= END_PAGE:
                continue

            text = page["text"]

            suspicious_spaces = []

            for i in range(1, len(text) - 1):
                previous_char = text[i - 1]
                current_char = text[i]
                next_char = text[i + 1]

                if (
                    current_char == " "
                    and is_arabic_letter(previous_char)
                    and is_arabic_letter(next_char)
                ):
                    suspicious_spaces.append(i)

            print(
                f"Page {page_number:3} | "
                f"characters: {len(text):4} | "
                f"suspicious spaces: {len(suspicious_spaces):3}"
            )


if __name__ == "__main__":
    analyze_spacing()