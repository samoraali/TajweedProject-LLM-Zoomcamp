# /// script
# dependencies = []
# ///

from pathlib import Path
import json


INPUT_PATH = Path("data/processed/cleaned_pages.jsonl")


def inspect_pages(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            record = json.loads(line)

            print("=" * 80)
            print(f"PDF PAGE: {record['pdf_page']}")
            print("=" * 80)
            print(record["text"])
            print()


if __name__ == "__main__":
    inspect_pages(INPUT_PATH)