"""Build retrieval-friendly JSONL from cleaned Tajweed OCR."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

TOPICS = [
    ("أحكام النون الساكنة والتنوين", ["النون الساكنة", "التنوين"]),
    ("الإظهار الحلقي", ["الإظهار الحلقي", "حروف الإظهار"]),
    ("الإدغام", ["الإدغام", "يرملون"]),
    ("الإقلاب", ["الإقلاب"]),
    ("الإخفاء الحقيقي", ["الإخفاء الحقيقي", "حروف الإخفاء"]),
    ("أحكام الميم الساكنة", ["الميم الساكنة"]),
    ("المدود", ["المدود", "المد الطبيعي", "المد الفرعي"]),
    ("المخارج والصفات", ["المخارج", "المخرج", "الغنة", "الخيشوم"]),
]

def topic(text):
    scores = [(sum(text.count(t) for t in terms), name)
              for name, terms in TOPICS]
    return max(scores)[1] if max(scores)[0] else "غير مصنف"

def keywords(text):
    vocab = set()
    for _, terms in TOPICS:
        vocab.update(t for t in terms if t in text)
    for t in ["الغنة", "الخيشوم", "النون", "الميم", "التنوين",
              "الإظهار", "الإدغام", "الإقلاب", "الإخفاء", "المخرج"]:
        if t in text:
            vocab.add(t)
    return sorted(vocab)

def chunks(text, limit):
    text = re.sub(r"^# PDF Page \d+\s*", "", text.strip())
    paragraphs = [x.strip() for x in re.split(r"\n\s*\n", text) if x.strip()]
    out, cur = [], ""
    for para in paragraphs:
        candidate = f"{cur}\n\n{para}".strip() if cur else para
        if len(candidate) <= limit:
            cur = candidate
        else:
            if cur:
                out.append(cur)
            cur = para
            if len(cur) > limit:
                parts = re.split(r"(?<=[.!؟؛])\s+", cur)
                cur = ""
                for part in parts:
                    candidate = f"{cur} {part}".strip() if cur else part
                    if len(candidate) <= limit:
                        cur = candidate
                    else:
                        if cur:
                            out.append(cur)
                        cur = part
    if cur:
        out.append(cur)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/ocr/cleaned")
    ap.add_argument("--output", default="data/knowledge_base/tajweed_kb.jsonl")
    ap.add_argument("--max-chars", type=int, default=1800)
    args = ap.parse_args()

    src, dst = Path(args.input), Path(args.output)
    files = sorted(src.glob("page_*.md"))
    if not files:
        raise SystemExit(f"No cleaned pages found in {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with dst.open("w", encoding="utf-8") as f:
        for path in files:
            page = int(re.search(r"page_(\d+)", path.stem).group(1))
            text = path.read_text(encoding="utf-8")
            for i, chunk in enumerate(chunks(text, args.max_chars)):
                rec = {
                    "id": f"tajweed-page-{page}-chunk-{i:03d}",
                    "source": "tajweed_book",
                    "pdf_page": page,
                    "topic": topic(text),
                    "keywords": keywords(text),
                    "text": chunk,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                count += 1
    print(f"Pages: {len(files)}")
    print(f"Chunks: {count}")
    print(f"KB: {dst.resolve()}")

if __name__ == "__main__":
    main()
