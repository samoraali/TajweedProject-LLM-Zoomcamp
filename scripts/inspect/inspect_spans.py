from pathlib import Path

import pymupdf


PDF_PATH = Path("data/raw/ملزمة التجويد 2024.pdf")
TARGET_PAGE = 120


def main():
    document = pymupdf.open(PDF_PATH)
    page = document[TARGET_PAGE - 1]

    data = page.get_text("dict")

    print("=" * 100)
    print(f"PDF PAGE: {TARGET_PAGE}")
    print("=" * 100)

    block_count = 0
    line_count = 0
    span_count = 0

    for block in data["blocks"]:
        if "lines" not in block:
            continue

        block_count += 1

        print(f"\n{'=' * 100}")
        print(f"BLOCK {block_count}")
        print(f"{'=' * 100}")

        for line in block["lines"]:
            line_count += 1

            print(
                f"\nLINE {line_count} "
                f"bbox={line['bbox']}"
            )

            for span in line["spans"]:
                span_count += 1

                print(
                    f"  SPAN {span_count}: "
                    f"bbox={span['bbox']} | "
                    f"size={span['size']:.1f} | "
                    f"text={span['text']!r}"
                )

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Blocks: {block_count}")
    print(f"Lines:  {line_count}")
    print(f"Spans:  {span_count}")


if __name__ == "__main__":
    main()