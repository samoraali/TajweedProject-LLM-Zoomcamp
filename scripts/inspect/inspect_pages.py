from pathlib import Path
import json


PAGES_PATH = Path("data/processed/pages.jsonl")

START_PAGE = 115
END_PAGE = 135


def load_pages():
    pages = {}

    with PAGES_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            page = json.loads(line)
            pages[page["pdf_page"]] = page["text"]

    return pages


def inspect_pages():
    pages = load_pages()

    for page_number in range(START_PAGE, END_PAGE + 1):
        text = pages.get(page_number, "")

        print("\n" + "=" * 100)
        print(f"PDF PAGE: {page_number}")
        print(f"CHARACTERS: {len(text)}")
        print("=" * 100)
        print(text[:4000])


if __name__ == "__main__":
    inspect_pages()