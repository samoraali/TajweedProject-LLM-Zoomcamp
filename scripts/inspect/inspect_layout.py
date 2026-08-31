from pathlib import Path

import pymupdf


PDF_PATH = Path("data/raw/ملزمة التجويد 2024.pdf")
TARGET_PAGE = 120


def main():
    document = pymupdf.open(PDF_PATH)

    page = document[TARGET_PAGE - 1]

    blocks = page.get_text("blocks")

    print("=" * 100)
    print(f"PDF PAGE: {TARGET_PAGE}")
    print(f"NUMBER OF BLOCKS: {len(blocks)}")
    print("=" * 100)

    for i, block in enumerate(blocks):
        x0, y0, x1, y1, text, block_number, block_type = block

        print(f"\nBLOCK {i}")
        print("-" * 100)
        print(f"Coordinates: ({x0:.1f}, {y0:.1f}) -> ({x1:.1f}, {y1:.1f})")
        print(f"Block number: {block_number}")
        print(f"Block type: {block_type}")
        print(f"Text: {text!r}")


if __name__ == "__main__":
    main()