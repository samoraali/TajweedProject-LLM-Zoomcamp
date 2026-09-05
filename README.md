# Tajweed AI Assistant

An Arabic-focused **Retrieval-Augmented Generation (RAG)** assistant for learning Tajweed (Quranic recitation rules), built as a capstone project for the **DataTalksClub LLM Zoomcamp**.

The assistant uses the source book **ملزمة التجويد 2024** to retrieve relevant passages and generate grounded Arabic answers.

## Project goal

The project builds an end-to-end pipeline that:

1. Extracts Tajweed material from the source PDF.
2. Cleans Arabic OCR output conservatively.
3. Organizes the material into a structured JSONL knowledge base.
4. Generates multilingual embeddings.
5. Retrieves candidate passages with semantic search.
6. Reranks candidates using lightweight Arabic lexical and topic signals.
7. Builds a grounded RAG prompt.
8. Generates an Arabic answer with an LLM.
9. Displays the source pages used for the answer.

## Current status

The core **data → retrieval → reranking → RAG generation** pipeline is working end to end.

A successful test produced an Arabic answer to:

> ما هو الإظهار الحلقي؟

and retrieved pages **120, 122, and 121**, all from the `الإظهار الحلقي` topic.

## Knowledge base

The current knowledge base contains:

- **21 cleaned source pages**
- **25 knowledge-base chunks**
- Topics:
  - أحكام النون الساكنة والتنوين
  - الإظهار الحلقي
  - الإدغام
  - الإقلاب
  - الإخفاء الحقيقي

The validated knowledge base is:

```text
data/processed/knowledge_base.jsonl
```

The original PDF is kept locally under `data/raw/` and is not committed to Git.

## Architecture

```text
                 ملزمة التجويد 2024
                         │
                         ▼
                 PDF / OCR Extraction
                         │
                         ▼
                  Arabic OCR Cleaning
                         │
                         ▼
                 Cleaned Markdown Pages
                         │
                         ▼
              Paragraph-aware Chunking
                         │
                         ▼
                knowledge_base.jsonl
                         │
                         ▼
              multilingual-e5-small
                         │
                         ▼
                  Semantic Search
                         │
                         ▼
                 Lightweight Reranking
                         │
                         ▼
                     Top 3 chunks
                         │
                         ▼
                  Grounded RAG Prompt
                         │
                         ▼
                       LLM
                         │
                         ▼
              Arabic answer + sources
```

## Retrieval

Semantic retrieval uses:

```text
intfloat/multilingual-e5-small
```

The implementation is in:

```text
src/tajweed_ai_assistant/retrieval/search.py
```

It:

1. Loads the JSONL knowledge base.
2. Embeds passages using the E5 passage format.
3. Embeds the Arabic query using the E5 query format.
4. Normalizes embeddings.
5. Computes cosine similarity.
6. Returns candidate passages.

The reranking layer is in:

```text
src/tajweed_ai_assistant/retrieval/rerank.py
```

It combines:

- semantic similarity
- normalized Arabic lexical overlap
- topic-aware bonuses

The final RAG pipeline retrieves **5 semantic candidates** and uses the best **3 reranked chunks** as LLM context.

## Retrieval evaluation

A 25-question Arabic retrieval test set covers the main Tajweed topics and comparison questions.

### Baseline semantic retrieval

| Metric | Result |
|---|---:|
| Hit@1 | **56%** |
| Hit@3 | **92%** |
| Hit@5 | **100%** |
| Topic@1 | **84%** |
| Topic@3 | **100%** |

### After lightweight reranking

| Metric | Result |
|---|---:|
| Hit@1 | **76%** |
| Hit@3 | **100%** |
| Hit@5 | **100%** |
| Topic@1 | **100%** |
| Topic@3 | **100%** |

The reranker improved Hit@1 from **56% to 76%** while preserving **100% Hit@3** and **100% Topic@1**. This is sufficient for the current RAG stage, where the top three chunks are passed to the generator.

Run the retrieval evaluation with:

```powershell
uv run python scripts/experiments/evaluate_retrieval.py
```

## RAG generation

The RAG layer is located in:

```text
src/tajweed_ai_assistant/rag/
```

### `prompt.py`

Builds:

- the Arabic grounding system prompt
- the retrieved context
- the final user prompt

The system prompt explicitly instructs the model to:

- answer in Arabic
- use the retrieved context only
- avoid unsupported additions
- avoid guessing
- say when the context is insufficient
- mention source pages when available

### `pipeline.py`

Connects:

```text
retrieval → reranking → context → prompt → generation
```

### `generator.py`

Uses the OpenAI Responses API to generate the final answer.

The API key is loaded from environment variables through `python-dotenv`.

## Setup

Clone the repository:

```powershell
git clone https://github.com/samoraali/TajweedProject-LLM-Zoomcamp.git
cd TajweedProject-LLM-Zoomcamp
```

Install dependencies:

```powershell
uv sync
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.6-luna
```

Never commit `.env` or an API key.

A safe template is provided as:

```text
.env.example
```

## Run the RAG test

The single-question end-to-end test is:

```powershell
uv run python scripts/test_rag.py
```

This loads the knowledge base and embedding model, retrieves the relevant context, generates an Arabic answer, and prints the source pages.

## Run the RAG evaluation questions

A small generation smoke-test suite is provided:

```powershell
uv run python scripts/experiments/evaluate_rag.py
```

It tests five representative questions covering:

- الإظهار الحلقي
- حروف الإظهار
- الإدغام
- الإقلاب
- الإخفاء الحقيقي

The script is intended for qualitative answer inspection rather than a fully automated factuality score.

## Run the interactive assistant

Start the CLI:

```powershell
uv run python scripts/chat.py
```

Example:

```text
Tajweed AI Assistant
اكتب سؤالك بالعربية. اكتب 'خروج' لإنهاء المحادثة.

السؤال: ما هو حرف الإقلاب؟

الإجابة:
...

المصادر:
- الصفحة 129 — الإقلاب
...
```

## Project structure

```text
tajweed-ai-assistant/
│
├── data/
│   ├── raw/
│   │   └── ملزمة التجويد 2024.pdf
│   ├── ocr/
│   │   └── cleaned/
│   │       ├── page_115.md
│   │       ├── ...
│   │       └── page_135.md
│   ├── processed/
│   │   └── knowledge_base.jsonl
│   └── review/
│       └── suspicious_ocr.json
│
├── scripts/
│   ├── chat.py
│   ├── test_rag.py
│   ├── experiments/
│   │   ├── evaluate_retrieval.py
│   │   ├── evaluate_rag.py
│   │   ├── ocr_experiment.py
│   │   └── ocr_test.py
│   └── inspect/
│       └── ...
│
├── src/
│   └── tajweed_ai_assistant/
│       ├── data_processing/
│       │   ├── build_knowledge_base.py
│       │   ├── clean_ocr.py
│       │   ├── extract.py
│       │   ├── extract_pymupdf.py
│       │   ├── ocr.py
│       │   └── repair_encoding.py
│       ├── rag/
│       │   ├── generator.py
│       │   ├── pipeline.py
│       │   └── prompt.py
│       └── retrieval/
│           ├── rerank.py
│           └── search.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Technology stack

- Python 3.14
- `uv`
- PyMuPDF
- Tesseract OCR
- Sentence Transformers
- `intfloat/multilingual-e5-small`
- NumPy
- OpenAI API
- `python-dotenv`
- JSONL
- Markdown

## Roadmap

### Data preparation

- [x] PDF extraction
- [x] PyMuPDF extraction
- [x] OCR experimentation
- [x] Extraction inspection
- [x] Arabic OCR cleaning
- [x] Knowledge-base construction
- [x] Knowledge-base validation
- [x] Retrieval evaluation dataset

### Retrieval

- [x] Generate embeddings
- [x] Implement semantic search
- [x] Evaluate retrieval quality
- [x] Add lightweight topic-aware reranking
- [x] Improve within-topic ranking
- [x] Evaluate reranked retrieval

### RAG

- [x] Connect retrieval to an LLM
- [x] Generate grounded Arabic answers
- [x] Include source/page references
- [x] Add unsupported-context instructions
- [x] Test representative RAG questions
- [ ] Expand automated answer-quality evaluation

### Application

- [x] Build a simple CLI interface
- [x] Connect the complete retrieval + RAG pipeline
- [x] Test end-to-end workflow
- [x] Document usage
- [ ] Optional web UI

## Notes on OCR quality

The source material contains some OCR noise. The cleaning pipeline is intentionally conservative: it fixes encoding and formatting problems without aggressively rewriting the source content.

The cleaned Markdown pages are treated as the canonical text used to build the knowledge base.

## Reproducibility

Raw/source documents and temporary extraction artifacts are excluded from version control. The validated knowledge base and project code are tracked so the retrieval/RAG system can be inspected and reproduced from the prepared data.

## Author

**Samar Ali**

DataTalksClub LLM Zoomcamp Capstone Project
