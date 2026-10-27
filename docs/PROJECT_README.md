# Aarogyasafa

A local-first medical document analysis MVP built with Python and FastAPI.

## Current features

- API health endpoint
- Text extraction from text-based PDFs
- Basic deterministic bill arithmetic checks
- Structured JSON responses
- Automated API tests

## Planned features

- OCR for scanned and multi-page documents
- Structured extraction of bills and discharge summaries
- Evidence-linked AI explanations
- Reviewed evaluation dataset and regression tests
- Secure document lifecycle and deletion
- Telegram integration through a separate adapter

## Setup

Python 3.10 or later is recommended.

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

On Windows PowerShell:

    .venv\\Scripts\\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

Start the API:

    uvicorn app.main:app --reload

Open the interactive API documentation at http://127.0.0.1:8000/docs.

Run tests:

    pytest -q

## Limitations

This is an early development foundation, not a clinical decision-support or
fraud-detection system. Scanned PDFs require OCR, and all findings should be
checked against original documents.

Do not upload sensitive patient documents to a public repository.
