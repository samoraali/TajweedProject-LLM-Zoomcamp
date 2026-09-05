"""Build retrieval-friendly JSONL from cleaned Tajweed OCR."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOPICS = [
    (
        "أحكام النون الساكنة والتنوين",
        ["أحكام النون الساكنة والتنوين", "النون الساكنة", "التنوين"],
    ),
    ("الإظهار الحلقي", ["الإظهار الحلقي", "حروف الإظهار"]),
    ("الإدغام", ["الإدغام", "حروف الإدغام", "يرملون"]),
    ("الإقلاب", ["الإقلاب"]),
    ("الإخفاء الحقيقي", ["الإخفاء الحقيقي", "حروف الإخفاء"]),
    ("أحكام الميم الساكنة", ["أحكام الميم الساكنة"]),
    ("الإظهار الشفوي", ["الإظهار الشفوي"]),
    ("الإخفاء الشفوي", ["الإخفاء الشفوي"]),
    ("إدغام مثلين صغير", ["إدغام مثلين صغير"]),
    ("اللامات", ["اللامات"]),
    ("لام التعريف", ["لام التعريف"]),
    ("لام الاسم", ["لام الاسم"]),
    ("لام الفعل", ["لام الفعل"]),
    ("لام الحرف", ["لام الحرف"]),
    ("لام الأمر", ["لام الأمر"]),
    ("المدود", ["المدود"]),
    ("المد الطبيعي", ["المد الطبيعي"]),
    ("المد الفرعي", ["المد الفرعي"]),
    ("المخارج والصفات", ["المخارج", "المخرج", "الغنة", "الخيشوم"]),
]


KEYWORDS = [
    "الغنة",
    "الخيشوم",
    "النون",
    "النون الساكنة",
    "الميم",
    "الميم الساكنة",
    "التنوين",
    "الإظهار",
    "الإظهار الحلقي",
    "الإظهار الشفوي",
    "الإدغام",
    "الإقلاب",
    "الإخفاء",
    "الإخفاء الحقيقي",
    "الإخفاء الشفوي",
    "المخارج",
    "المخرج",
    "اللامات",
    "لام التعريف",
    "لام الاسم",
    "لام الفعل",
    "لام الحرف",
    "لام الأمر",
    "المدود",
    "المد",
    "المد الطبيعي",
    "المد الفرعي",
]


def normalize_text(text: str) -> str:
    """Normalize whitespace without changing Arabic wording."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\ufeff", "")
    text = text.replace("\u200e", "")
    text = text.replace("\u200f", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def detect_explicit_topic(text: str) -> str | None:
    """
    Prefer explicit section headings over keyword frequency.

    This prevents a page about الإظهار الحلقي from being classified
    as the broader أحكام النون الساكنة والتنوين simply because
    the page mentions النون الساكنة many times.
    """
    # Check longer/specific topics first.
    ordered_topics = sorted(
        TOPICS,
        key=lambda item: max(len(term) for term in item[1]),
        reverse=True,
    )

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:8]:
        cleaned = re.sub(r"^[#>*\-©|.\s]+", "", line).strip()

        for topic, terms in ordered_topics:
            for term in terms:
                if term in cleaned and len(cleaned) <= 120:
                    return topic

    return None

def detect_page_topic(pdf_page: int, text: str) -> str:
    """Infer the main Tajweed topic for a PDF page."""

    if pdf_page == 115:
        return "فهرس / نظرة عامة"

    if 116 <= pdf_page <= 119:
        return "أحكام النون الساكنة والتنوين"

    if 120 <= pdf_page <= 122:
        return "الإظهار الحلقي"

    if 123 <= pdf_page <= 128:
        return "الإدغام"

    if 129 <= pdf_page <= 131:
        return "الإقلاب"

    if 132 <= pdf_page <= 135:
        return "الإخفاء الحقيقي"

    return detect_topic(text)

def detect_topic(text: str) -> str:
    """Assign the most specific Tajweed topic to a chunk."""

    # Handle the table-of-contents page first.
    if "الباب الثانى" in text and "المدود" in text:
        return "فهرس / نظرة عامة"
    
    # Most specific topics first.
    explicit_topics = [
        ("الإظهار الحلقي", ["الإظهار الحلقي"]),
        ("الإدغام", ["الإدغام"]),
        ("الإقلاب", ["الإقلاب"]),
        ("الإخفاء الحقيقي", ["الإخفاء الحقيقي"]),
        ("الإظهار الشفوي", ["الإظهار الشفوي"]),
        ("الإخفاء الشفوي", ["الإخفاء الشفوي"]),
        ("إدغام مثلين صغير", ["إدغام مثلين صغير"]),
        ("لام التعريف", ["لام التعريف"]),
        ("لام الاسم", ["لام الاسم"]),
        ("لام الفعل", ["لام الفعل"]),
        ("لام الحرف", ["لام الحرف"]),
        ("لام الأمر", ["لام الأمر"]),
        ("المد الطبيعي", ["المد الطبيعي"]),
        ("المد الفرعي", ["المد الفرعي"]),
        ("المدود", ["المدود"]),
        ("أحكام الميم الساكنة", ["أحكام الميم الساكنة"]),
        (
            "أحكام النون الساكنة والتنوين",
            ["أحكام النون الساكنة والتنوين"],
        ),
    ]

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # First look for explicit topic headings anywhere in the chunk.
    for topic, terms in explicit_topics:
        for line in lines:
            cleaned = re.sub(
                r"^[#>*\-©|.\s]+",
                "",
                line,
            ).strip()

            if any(term in cleaned for term in terms):
                return topic

    # Fall back to keyword scoring only if no explicit heading exists.
    scores = [
        (sum(text.count(term) for term in terms), topic)
        for topic, terms in TOPICS
    ]

    best_score, best_topic = max(
        scores,
        key=lambda item: item[0],
    )

    return best_topic if best_score else "غير مصنف"


def extract_keywords(text: str) -> list[str]:
    """Extract known Tajweed keywords appearing in the chunk."""
    return sorted(
        {keyword for keyword in KEYWORDS if keyword in text},
        key=len,
        reverse=True,
    )


def split_long_text(text: str, limit: int) -> list[str]:
    """Split long text using sentence boundaries where possible."""
    if len(text) <= limit:
        return [text]

    sentences = re.split(r"(?<=[.!؟؛:])\s+", text)

    result: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        candidate = (
            f"{current} {sentence}".strip()
            if current
            else sentence
        )

        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                result.append(current)

            if len(sentence) > limit:
                result.extend(
                    sentence[start : start + limit]
                    for start in range(0, len(sentence), limit)
                )
                current = ""
            else:
                current = sentence

    if current:
        result.append(current)

    return result


def is_section_heading(line: str) -> bool:
    """
    Detect likely section headings in OCR output.

    We intentionally keep this conservative because OCR text can
    contain punctuation/noise around headings.
    """
    line = line.strip()

    if not line:
        return False

    cleaned = re.sub(r"^[#>*\-©|.\s]+", "", line).strip()

    if not cleaned:
        return False

    # Markdown headings.
    if line.startswith("#"):
        return True

    # Known explicit Tajweed headings.
    heading_phrases = [
        "أحكام النون الساكنة والتنوين",
        "النون الساكنة",
        "التنوين",
        "الإظهار الحلقي",
        "الإدغام",
        "الإقلاب",
        "الإخفاء الحقيقي",
        "أحكام الميم الساكنة",
        "الإظهار الشفوي",
        "الإخفاء الشفوي",
        "إدغام مثلين صغير",
        "اللامات",
        "لام التعريف",
        "لام الاسم",
        "لام الفعل",
        "لام الحرف",
        "لام الأمر",
        "المدود",
        "المد الطبيعي",
        "المد الفرعي",
        "المخارج",
    ]

    if any(phrase in cleaned for phrase in heading_phrases):
        return len(cleaned) <= 120

    # Question-style headings are useful retrieval boundaries.
    if cleaned.startswith(("لماذا", "ما سبب", "ما هو", "ما هي", "كيف", "اذكري", "اذكر")):
        return True

    return False


def build_sections(text: str) -> list[str]:
    """
    Split OCR into logical sections using headings and blank lines.

    This is important for pages such as page 115 where OCR uses
    single newlines instead of blank lines between sections.
    """
    lines = text.splitlines()

    sections: list[str] = []
    current: list[str] = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if current:
                sections.append("\n".join(current).strip())
                current = []
            continue

        if current and is_section_heading(stripped):
            sections.append("\n".join(current).strip())
            current = [stripped]
        else:
            current.append(stripped)

    if current:
        sections.append("\n".join(current).strip())

    return [section for section in sections if section]


def chunks(text: str, limit: int) -> list[str]:
    """Create retrieval-sized chunks while preserving section boundaries."""
    text = re.sub(
        r"^# PDF Page \d+\s*",
        "",
        text.strip(),
        flags=re.MULTILINE,
    )

    sections = build_sections(text)

    output: list[str] = []
    current = ""

    for section in sections:
        parts = split_long_text(section, limit)

        for part in parts:
            candidate = (
                f"{current}\n\n{part}".strip()
                if current
                else part
            )

            if len(candidate) <= limit:
                current = candidate
            else:
                if current:
                    output.append(current)

                current = part

    if current:
        output.append(current)

    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build retrieval-friendly JSONL from cleaned Tajweed OCR."
    )

    parser.add_argument(
        "--input",
        default="data/ocr/cleaned",
    )

    parser.add_argument(
        "--output",
        default="data/processed/knowledge_base.jsonl",
    )

    parser.add_argument(
        "--max-chars",
        type=int,
        default=1500,
    )

    args = parser.parse_args()

    source_dir = Path(args.input)
    output_path = Path(args.output)

    files = sorted(source_dir.glob("page_*.md"))

    if not files:
        raise SystemExit(
            f"No cleaned pages found in {source_dir}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    record_count = 0

    with output_path.open("w", encoding="utf-8") as output_file:
        for path in files:
            match = re.search(
                r"page_(\d+)",
                path.stem,
            )

            if not match:
                continue

            pdf_page = int(match.group(1))

            text = normalize_text(
                path.read_text(encoding="utf-8")
            )

            page_chunks = chunks(
                text,
                args.max_chars,
            )

            for chunk_index, chunk_text in enumerate(page_chunks):
                record = {
                    "id": (
                        f"tajweed-page-{pdf_page}"
                        f"-chunk-{chunk_index:03d}"
                    ),
                    "source": "tajweed_book",
                    "pdf_page": pdf_page,
                    "chunk_index": chunk_index,
                    "topic": detect_page_topic(pdf_page, text),
                    "keywords": extract_keywords(chunk_text),
                    "text": chunk_text,
                }

                output_file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

                record_count += 1

    print("=" * 60)
    print("KNOWLEDGE BASE BUILT")
    print("=" * 60)
    print(f"Pages:  {len(files)}")
    print(f"Chunks: {record_count}")
    print(f"Output: {output_path.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()