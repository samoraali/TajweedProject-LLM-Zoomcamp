from pathlib import Path
import json

import pymupdf


PDF_PATH = Path("data/raw/ملزمة التجويد 2024.pdf")
OUTPUT_PATH = Path("data/processed/pymupdf_pages.jsonl")


def extract_pages(pdf_path: Path, output_path: Path) -> None:
    document = pymupdf.open(pdf_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for page_num, page in enumerate(document):
            text = page.get_text("text")

            record = {
                "pdf_page": page_num + 1,
                "text": text,
                "source": pdf_path.name,
                "extractor": "pymupdf",
            }

            f.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    print(
        f"Extracted {len(document)} pages to {output_path}"
    )


if __name__ == "__main__":
    extract_pages(PDF_PATH, OUTPUT_PATH)