from pathlib import Path

import fitz


PDF_PATH = Path("data/raw/ملزمة التجويد 2024.pdf")

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


def main():
    document = fitz.open(PDF_PATH)

    total_characters = 0
    total_suspicious_spaces = 0

    for page_number in range(START_PAGE, END_PAGE + 1):
        page = document[page_number - 1]

        text = page.get_text("text")

        suspicious_spaces = count_suspicious_spaces(text)

        total_characters += len(text)
        total_suspicious_spaces += suspicious_spaces

        print(
            f"Page {page_number:3} | "
            f"characters: {len(text):4} | "
            f"suspicious spaces: {suspicious_spaces:3}"
        )

    print("\n" + "=" * 60)
    print("TOTAL")
    print("=" * 60)
    print(f"Characters:        {total_characters}")
    print(f"Suspicious spaces: {total_suspicious_spaces}")


if __name__ == "__main__":
    main()