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
Embeddings / Vector Search
    │
    ▼
RAG Question Answering

