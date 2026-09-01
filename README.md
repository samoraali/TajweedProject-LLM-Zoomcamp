# Tajweed AI Assistant

An AI-powered assistant for answering questions about **Tajweed (Quranic recitation rules)** using a retrieval-augmented generation (RAG) approach.

The project is being developed as part of the **DataTalksClub LLM Zoomcamp**.

## Project Goal

The goal of this project is to build an Arabic-focused question-answering assistant that can retrieve relevant Tajweed material from a source book and use that material to provide grounded answers.

The initial source is:

> ملزمة التجويد 2024

The project focuses on building a reliable data pipeline for extracting, cleaning, organizing, and eventually retrieving Tajweed knowledge.

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
- Added an initial OCR cleaning pipeline.
- Added an initial knowledge-base builder.
- Added Git version control and pushed the current project history to GitHub.

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

## Project Structure

```text
tajweed-ai-assistant/
├── data/
│   ├── raw/
│   ├── intermediate/
│   ├── processed/
│   └── review/
├── scripts/
│   ├── experiments/
│   └── inspect/
├── src/
│   └── tajweed_ai_assistant/
│       └── data_processing/
├── pyproject.toml
├── uv.lock
└── README.md


### 2. Add 'Technology Stack'

Keep it simple for now:

```markdown
## Technology Stack

- Python
- uv — Python project and dependency management
- PyMuPDF — PDF text extraction
- Tesseract OCR — OCR for difficult pages
- JSONL — intermediate and knowledge-base data format
- Embeddings — planned
- Vector database — planned
- LLM — planned

## Roadmap

### Data Preparation
- [x] PDF extraction
- [x] PyMuPDF extraction
- [x] OCR experimentation
- [x] Extraction inspection
- [x] Initial OCR cleaning
- [x] Initial knowledge-base builder
- [ ] Improve OCR cleaning
- [ ] Validate knowledge-base chunks

### Retrieval
- [ ] Generate embeddings
- [ ] Set up vector database
- [ ] Implement semantic search
- [ ] Evaluate retrieval quality

### RAG
- [ ] Connect retrieval to an LLM
- [ ] Generate grounded Arabic answers
- [ ] Include source/page references
- [ ] Evaluate answer quality

### Application
- [ ] Build a simple interface
- [ ] Test end-to-end workflow
- [ ] Document usage

## Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/samoraali/TajweedProject-LLM-Zoomcamp.git
cd TajweedProject-LLM-Zoomcamp
uv sync