# /// script
# dependencies = [
#     "pypdfium2>=4.0.0",
# ]
# ///

from pathlib import Path
import json
import pypdfium2 as pdfium

PDF_PATH = Path("data/raw/ملزمة التجويد 2024.pdf")
OUTPUT_PATH = Path("data/processed/raw_pages.jsonl")

def extract_pages(pdf_path: Path, output_path: Path) -> None:
    # Open the PDF document
    pdf = pdfium.PdfDocument(pdf_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text_page = page.get_textpage()
            
            # Extract text preserving reading flow
            text = text_page.get_text_range()

            record = {
                "pdf_page": page_num + 1,
                "text": text
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Extracted {len(pdf)} pages to {output_path}")

if __name__ == "__main__":
    extract_pages(PDF_PATH, OUTPUT_PATH)