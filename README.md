# Tajweed AI Assistant

An AI-powered assistant for answering questions about **Tajweed (Quranic recitation rules)** using a retrieval-augmented generation (RAG) approach.

The project is being developed as part of the **DataTalksClub LLM Zoomcamp**.

## Project Goal

The goal of this project is to build an Arabic-focused question-answering assistant that can retrieve relevant Tajweed material from a source book and use that material to provide grounded answers.

The initial source is:

> ملزمة التجويد 2024

The project focuses on building a reliable pipeline for:

1. Extracting Tajweed material from the source PDF
2. Cleaning Arabic OCR output
3. Organizing the material into a structured knowledge base
4. Generating embeddings
5. Retrieving relevant passages
6. Reranking retrieved passages
7. Using retrieved context to generate grounded Arabic answers with an LLM

---

## Current Progress

The project is currently in the **data preparation and knowledge-base pipeline stage**.

### Completed

- Created the Python project structure.
- Configured the project using `pyproject.toml`.
- Set up the project environment with `uv`.
- Added dependency locking through `uv.lock`.
- Added the source Tajweed PDF to the local data pipeline.
- Implemented PDF text extraction.
- Implemented an alternative PyMuPDF extraction pipeline for comparison.
- Added OCR processing for pages where text extraction is insufficient.
- Added scripts for inspecting and comparing extracted text.
- Investigated Arabic text layout, spacing, characters, and OCR output.
- Added an Arabic OCR cleaning pipeline.
- Created cleaned Markdown pages for the relevant source pages.
- Built a structured knowledge base in JSONL format.
- Added semantic retrieval using Sentence Transformers.
- Added retrieval evaluation using Arabic test queries.
- Evaluated retrieval on 25 Arabic queries covering the main Tajweed topics.

### Current Knowledge Base

The current knowledge base contains:

- **21 cleaned source pages**
- **25 knowledge-base chunks**
- Source pages covering:
  - أحكام النون الساكنة والتنوين
  - الإظهار الحلقي
  - الإدغام
  - الإقلاب
  - الإخفاء الحقيقي

The knowledge base is stored at:

```text
data/processed/knowledge_base.jsonl
```

### Retrieval Baseline
Semantic retrieval is currently implemented using: 
``` 
intfloat/multilingual-e5-small 
```
### Current Evaluation
A test set of **25 Arabic queries** was created to evaluate retrieval quality.

Current baseline results: 
| **Metric** | **Result** |
|:-----------|------------|
| Hit@1 | **56%** |
| Hit@3 | **92%** |
| Hit@5 | **100%** |
| Topic@1 | **84%** |
| Topic@3 | **100%** |

These results show that the current embedding-based retrieval is effective at finding the correct Tajweed topic and generating a strong set of candidate passages.

The main remaining retrieval problem is **within-topic ranking**. In several queries, the correct page appears in the top 3 or top 5 but not ranked first.

The next retrieval improvement will therefore focus on lightweight **topic-aware and lexical reranking** rather than immediately replacing the embedding model.

### Current Pipeline

The current data-processing workflow is:

```text
Tajweed PDF
    │
    ▼
PDF Text Extraction
    │
    ├── PyMuPDF extraction
    │
    └── OCR extraction
    │
    ▼
Extracted Page Data
    │
    ▼
OCR Cleaning
    │
    ▼
Cleaned Pages
    │
    ▼
Knowledge Base
    │
    ▼
Embeddings
    │
    ▼
Vector Search
    │
    ▼
Retrieved Context
    │
    ▼
LLM
    │
    ▼
RAG Question Answering 

```
## Data and Reproducibility

The initial knowledge source is:

> ملزمة التجويد 2024

The source PDF is kept locally under `data/raw/` and is not committed to Git because of its file size and source-document considerations.

Generated data under `data/processed/` is also excluded from version control. The processing pipeline can regenerate these files from the source document.

### Knowledge-Base Pipeline

```text
Tajweed PDF
    │
    ▼
PDF / OCR Extraction
    │
    ▼
Extracted Pages
    │
    ▼
Conservative Arabic OCR Cleaning
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
Embeddings
    │
    ▼
Semantic Search

```
## Project Structure

```text
tajweed-ai-assistant/

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
│   ├── experiments/
│   │   ├── evaluate_retrieval.py
│   │   ├── ocr_experiment.py
│   │   └── ocr_test.py
│   │
│   └── inspect/
│       ├── analyze_pymupdf.py
│       ├── analyze_raw_pages.py
│       ├── analyze_spacing.py
│       ├── compare_extractors.py
│       ├── inspect_chars.py
│       ├── inspect_cleaned_ocr.py
│       ├── inspect_layout.py
│       ├── inspect_pages.py
│       ├── inspect_pymupdf.py
│       └── inspect_spans.py
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
│       │
│       └── retrieval/
│           ├── __init__.py
│           └── search.py
│
├── pyproject.toml
├── uv.lock
└── README.md

```
## Technology Stack

- Python
- uv — Python project and dependency management
- PyMuPDF — PDF text extraction
- Tesseract OCR — OCR for difficult pages
- Sentence Transformers — text embeddings and semantic retrieval
- intfloat/multilingual-e5-small — multilingual embedding model
- NumPy — embedding normalization and similarity calculations
- JSONL — knowledge-base storage format
- LLM — planned for the RAG generation stage

## Retrieval

The current retrieval implementation is located at: 
``` bash
src/tajweed_ai_assistant/retrieval/search.py
```
It: 
1. Loads the knowledge base.
2. Creates embeddings for knowledge-base passages.
3. Embeds the user's Arabic query.
4. Normalizes the embeddings.
5. Calculates cosine similarity.
6. Returns the highest-ranking passages.

A retieval evaluation script is available at: 
``` bash
scripts/experiments/evaluate_retrieval.py
```

The evaluation currently uses 25 Arabic test queries covering: 
- الإظهار الحلقي
- الإدغام
- الإقلاب
- الإخفاء الحقيقي
- General comparison between Tajweed rules

## Roadmap

### Data Preparation
- [x] PDF extraction
- [x] PyMuPDF extraction
- [x] OCR experimentation
- [x] Extraction inspection
- [x]  Arabic OCR cleaning
- [x] Knowledge-base construction
- [x] Knowledge-base validation
- [x] Create retrieval evaluation dataset

### Retrieval
- [x] Generate embeddings
- [x] Implement semantic search
- [x] Evaluate retrieval quality
- [x] Add lightweight topic-aware reranking
- [x] Improve within-topic ranking
- [x] Consider vector database integration
- [x] Expand retrieval evaluation

### RAG
- [ ] Connect retrieval to an LLM
- [ ] Generate grounded Arabic answers
- [ ] Generate grounded Arabic answers
- [ ] Include source/page references
- [ ] Evaluate answer quality
- [ ] Test unsupported/out-of-scope questions

### Application
- [ ] Build a simple interface
- [ ] Connect the complete retrieval + RAG pipeline
- [ ] Test end-to-end workflow
- [ ] Document usage

## Setup

Clone the repository and install the dependencies:

``` bash
git clone https://github.com/samoraali/TajweedProject-LLM-Zoomcamp.git
cd TajweedProject-LLM-Zoomcamp
uv sync
```
### Running Retrieval 
Run the semantic retrieval CLI with: 
``` bash
uv run python -m tajweed_ai_assistant.retrieval.search "ما هي حروف الإقلاب؟"
```

For example, to retrieve the top 5 results: 
``` bash
uv run python -m tajweed_ai_assistant.retrieval.search "ما هي حروف الإقلاب؟"
```

### Running Retrieval Evaluation
Run the current 25-query evaluation with: 
``` bash
uv run python scripts/experiments/evaluate_retrieval.py
```
The evaluation reports Hit@, Hit@3, Hit@55, Topic@1, and Topic@3.

### Project Status
The project iscurrently between the **retrieval baseline** and **RAG implementation** stages.

The data pipeline and initial semantic retrieval system are working. The next major step is to improve retrieval ranking with lightweight reranking, then connect the retrieved context to an LLM for grounded Arabic Tajweed queestion answering.

### **Author**
**Samar Ali**

DataTalkClu LLM Zoomcamp Capstone Project