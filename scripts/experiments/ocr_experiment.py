# /// script
# dependencies = [
#     "pytesseract>=0.3.13",
#     "pymupdf>=1.24.0",
#     "pillow>=10.0.0",
# ]
# ///

from pathlib import Path
import json

import fitz
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

PDF_PATH = Path("data/raw/ملزمة التجويد 2024.pdf")
OUTPUT_PATH = Path("data/processed/ocr_pages_fresh.jsonl")

START_PAGE = 115
END_PAGE = 135


def ocr_page(pdf, pdf_page_number: int) -> str:
    """Render one PDF page and run Arabic OCR."""

    # PyMuPDF uses zero-based page indexes.
    page = pdf[pdf_page_number - 1]

    # Higher resolution gives Tesseract more detail to work with.
    matrix = fitz.Matrix(2.5, 2.5)
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
    print("TAJWEED OCR EXPERIMENT")
    print("=" * 70)
    print(f"PDF:        {PDF_PATH}")
    print(f"Pages:      {START_PAGE}-{END_PAGE}")
    print(f"Output:     {OUTPUT_PATH}")
    print("=" * 70)
    print()

    pdf = fitz.open(PDF_PATH)

    try:
        with OUTPUT_PATH.open("w", encoding="utf-8") as output_file:

            for page_number in range(START_PAGE, END_PAGE + 1):

                print(f"OCR page {page_number}...", end=" ", flush=True)

                text = ocr_page(pdf, page_number)

                record = {
                    "pdf_page": page_number,
                    "text": text,
                }

                output_file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

                print(f"{len(text)} characters")

    finally:
        pdf.close()

    print()
    print("=" * 70)
    print("OCR COMPLETE")
    print("=" * 70)
    print(f"Pages processed: {END_PAGE - START_PAGE + 1}")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()