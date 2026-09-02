"""Repair known Arabic mojibake in OCR JSONL."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def repair_text(text: str) -> str:
    """
    Repair Arabic text that was corrupted into patterns such as:

        ط§ظ„ط¨ط§ط¨

    which should become:

        الباب

    The transformation is intentionally limited to the known
    mojibake marker characters before the UTF-8 recovery step.
    """
    # Recover the characters that represent the original UTF-8 byte
    # sequences in this specific corruption pattern.
    text = text.replace("ط", "Ø")
    text = text.replace("ظ", "Ù")

    try:
        return text.encode("cp1252").decode("utf-8")
    except UnicodeError:
        # If a page contains legitimate characters that prevent the
        # full round-trip, return the original text rather than
        # silently damaging it.
        return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/processed/ocr_pages.jsonl",
    )
    parser.add_argument(
        "--output",
        default="data/processed/ocr_pages_repaired.jsonl",
    )
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output)

    if not src.exists():
        raise SystemExit(f"Missing input file: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    changed = 0

    with (
        src.open("r", encoding="utf-8") as fin,
        dst.open("w", encoding="utf-8") as fout,
    ):
        for line in fin:
            if not line.strip():
                continue

            record = json.loads(line)
            original = record.get("text", "")
            repaired = repair_text(original)

            if repaired != original:
                changed += 1

            record["text"] = repaired
            fout.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            total += 1

    print(f"Records: {total}")
    print(f"Changed: {changed}")
    print(f"Output:  {dst.resolve()}")


if __name__ == "__main__":
    main()