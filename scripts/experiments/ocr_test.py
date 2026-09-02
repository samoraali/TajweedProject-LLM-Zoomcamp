from pathlib import Path
import json

import fitz
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Find the PDF without relying on its corrupted filename.
PDF_DIR = Path("data/raw")
PDF_PATH = next(PDF_DIR.glob("*.pdf"))

OUTPUT_PATH = Path("data/processed/ocr_test.jsonl")

START_PAGE = 115
END_PAGE = 135


def ocr_page(pdf, pdf_page_number: int) -> str:
    """Render one PDF page and run Arabic OCR."""

    page = pdf[pdf_page_number - 1]

    # Render at higher resolution.
    matrix = fitz.Matrix(3, 3)
    pixmap = page.get_pixmap(matrix=matrix)

    image = Image.frombytes(
        "RGB",
        [pixmap.width, pixmap.height],
        pixmap.samples,
    )

    text = pytesseract.image_to_string(
        image,
        lang="ara",
        config="--psm 6",
    )

    return text.strip()


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("TAJWEED OCR TEST")
    print("=" * 70)
    print(f"PDF:    {PDF_PATH}")
    print(f"Page:   {START_PAGE}")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 70)

    pdf = fitz.open(PDF_PATH)

    try:
        text = ocr_page(pdf, START_PAGE)

        record = {
            "pdf_page": START_PAGE,
            "text": text,
        }

        with OUTPUT_PATH.open("w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

        print()
        print("OCR RESULT")
        print("=" * 70)
        print(text)
        print("=" * 70)
        print(f"Characters: {len(text)}")

    finally:
        pdf.close()


if __name__ == "__main__":
    main()