"""Conservative Arabic OCR cleaner. Raw OCR is never overwritten."""
from __future__ import annotations
import argparse, json, re, unicodedata
from pathlib import Path

GARBAGE = {
    "\uf07b": "", "\uf07c": "", "\uf07d": "", "\uf07e": "",
    "\uf0a9": "", "\uf0b7": "•", "\u200b": "", "\u200c": "",
    "\u200d": "", "\ufeff": "",
}

TERMS = [
    "النون الساكنة", "التنوين", "الإظهار", "الإظهار الحلقي",
    "الإدغام", "الإدغام الكامل", "الإدغام الناقص",
    "الإقلاب", "الإخفاء", "الإخفاء الحقيقي", "الغنة",
    "الخيشوم", "المخرج", "المخارج", "يرملون",
]

PATTERNS = [
    r"[إأآا]إ[إأآا]",
    r"[A-Za-z]{3,}",
    r"[<>]{2,}|[=]{3,}|[_]{3,}",
    r"([ء-ي])\1{2,}",
]

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    for a, b in GARBAGE.items():
        text = text.replace(a, b)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("ـ", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+([،؛؟:,.])", r"\1", text)
    text = re.sub(r"([،؛؟:])(?=[^\s\n])", r"\1 ", text)
    return text.strip()

def suspicious(text: str) -> list[dict]:
    result = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for token in line.split():
            reasons = []
            if len(token) > 25:
                reasons.append("very_long_token")
            for p in PATTERNS:
                if re.search(p, token):
                    reasons.append(p)
            if reasons:
                result.append({"line": line_no, "token": token, "reasons": reasons})
    return result

def load_pages(folder: Path):
    pages = []
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() == ".json":
            try:
                d = json.loads(p.read_text(encoding="utf-8-sig"))
            except Exception as e:
                print(f"WARNING: {p}: {e}")
                continue
            page = d.get("pdf_page", d.get("page"))
            text = d.get("text", "")
            if page is not None and text:
                pages.append((int(page), str(text), p.name))
        elif p.suffix.lower() == ".txt":
            m = re.search(r"(\d+)", p.stem)
            if m:
                pages.append((int(m.group(1)),
                              p.read_text(encoding="utf-8-sig"), p.name))
    return sorted(pages)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/ocr/raw")
    ap.add_argument("--output", default="data/ocr/cleaned")
    ap.add_argument("--review", default="data/review/suspicious_ocr.json")
    args = ap.parse_args()

    src, dst, review = map(Path, (args.input, args.output, args.review))
    if not src.exists():
        raise SystemExit(f"Missing input folder: {src}")

    dst.mkdir(parents=True, exist_ok=True)
    review.parent.mkdir(parents=True, exist_ok=True)

    pages = load_pages(src)
    if not pages:
        raise SystemExit(f"No .json/.txt OCR pages found in {src}")

    report = []
    for page, raw, source in pages:
        cleaned = normalize(raw)
        (dst / f"page_{page:03d}.md").write_text(
            f"# PDF Page {page}\n\n{cleaned}\n", encoding="utf-8"
        )
        report.append({
            "pdf_page": page,
            "source_file": source,
            "tajweed_terms_found": [t for t in TERMS if t in cleaned],
            "suspicious": suspicious(cleaned),
        })

    review.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    print(f"Processed {len(pages)} pages.")
    print(f"Cleaned: {dst.resolve()}")
    print(f"Review:  {review.resolve()}")

if __name__ == "__main__":
    main()
