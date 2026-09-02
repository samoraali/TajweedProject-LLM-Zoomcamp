"""Conservative cleaner for Arabic Tajweed OCR."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def normalize(text: str) -> str:
    """Normalize whitespace without changing Arabic words."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove zero-width / BOM characters.
    text = text.replace("\ufeff", "")
    text = text.replace("\u200b", "")
    text = text.replace("\u200c", "")
    text = text.replace("\u200d", "")

    # Normalize spaces.
    text = re.sub(r"[ \t]+", " ", text)

    # Clean excessive blank lines.
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_pages(path: Path) -> list[dict]:
    """Load OCR pages from JSONL."""
    pages = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"WARNING: invalid JSON on line {line_number}: {e}")
                continue

            page = record.get("pdf_page")
            text = record.get("text", "")

            if page is None or not text:
                continue

            pages.append(
                {
                    "pdf_page": int(page),
                    "text": str(text),
                }
            )

    return pages


def find_suspicious_lines(text: str) -> list[dict]:
    """Flag possible OCR problems for human review."""
    results = []

    suspicious_terms = [
        "التون",
        "ققَاء",
        "ققًا",
        "غبر",
        "زىئ",
    ]

    for line_number, line in enumerate(text.splitlines(), 1):
        for term in suspicious_terms:
            if term in line:
                results.append(
                    {
                        "line": line_number,
                        "term": term,
                        "text": line,
                    }
                )

    return results


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="data/processed/ocr_pages_fresh.jsonl",
    )

    parser.add_argument(
        "--output",
        default="data/ocr/cleaned",
    )

    parser.add_argument(
        "--review",
        default="data/review/suspicious_ocr.json",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    review_path = Path(args.review)

    if not input_path.exists():
        raise SystemExit(f"Missing input file: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    review_path.parent.mkdir(parents=True, exist_ok=True)

    pages = load_pages(input_path)

    if not pages:
        raise SystemExit("No OCR pages found.")

    review = []

    for page in pages:
        pdf_page = page["pdf_page"]
        raw_text = page["text"]

        cleaned = normalize(raw_text)

        output_file = output_dir / f"page_{pdf_page:03d}.md"

        output_file.write_text(
            f"# PDF Page {pdf_page}\n\n{cleaned}\n",
            encoding="utf-8",
        )

        review.append(
            {
                "pdf_page": pdf_page,
                "suspicious": find_suspicious_lines(cleaned),
            }
        )

    review_path.write_text(
        json.dumps(review, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Processed {len(pages)} pages.")
    print(f"Cleaned: {output_dir.resolve()}")
    print(f"Review:  {review_path.resolve()}")


if __name__ == "__main__":
    main()