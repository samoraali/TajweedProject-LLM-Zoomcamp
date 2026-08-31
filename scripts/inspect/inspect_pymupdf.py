from pathlib import Path
import json


PAGES_PATH = Path("data/processed/pymupdf_pages.jsonl")
TARGET_PAGE = 120


def main():
    with PAGES_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            page = json.loads(line)

            if page["pdf_page"] == TARGET_PAGE:
                print("=" * 80)
                print(f"PDF PAGE: {TARGET_PAGE}")
                print("=" * 80)
                print(page["text"])
                return

    print(f"Page {TARGET_PAGE} not found.")


if __name__ == "__main__":
    main()