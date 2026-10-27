# Aarogyasafa architecture

## Initial request flow

1. A client submits a PDF to the FastAPI application.
2. The document parser extracts embedded text.
3. The API returns extracted text and a processing status.
4. A separate bill-audit endpoint accepts structured line items.
5. Deterministic arithmetic checks return review findings.

## Planned components

- OCR service for scanned and multi-page documents.
- Extraction service for structured bill and discharge-summary fields.
- Analysis engine with validated LLM outputs and source evidence.
- Evaluation pipeline using reviewed, de-identified documents.
- Optional Telegram adapter calling the same analysis service.

## Safety and privacy

- Do not commit real patient documents or credentials.
- Keep the analysis engine independent of messaging providers.
- Treat automated findings as potential discrepancies requiring review.
- The development API is not production-hardened and must not be exposed publicly
  without authentication, access controls, and appropriate document-retention
  and deletion safeguards.
