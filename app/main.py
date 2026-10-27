from fastapi import FastAPI, File, HTTPException, UploadFile

from app.schemas import (
    BillAuditRequest,
    BillAuditResponse,
    DocumentAnalysis,
    HealthResponse,
)
from app.services.bill_audit import audit_bill
from app.services.document_parser import extract_pdf_text

app = FastAPI(
    title="Aarogyasafa API",
    version="0.1.0",
    description="Local-first medical document analysis MVP",
)

MAX_FILE_SIZE = 10 * 1024 * 1024


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", app="Aarogyasafa")


@app.post("/api/v1/documents/analyze", response_model=DocumentAnalysis)
async def analyze_document(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=415,
                detail="Only PDF documents are supported currently.",
            )

        content = await file.read(MAX_FILE_SIZE + 1)
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF exceeds the 10 MB limit.",
            )

        try:
            text = extract_pdf_text(content)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return DocumentAnalysis(
            filename=file.filename or "document.pdf",
            extracted_text=text,
            status="text_extracted",
            message="Text extraction succeeded. AI analysis has not yet been performed.",
        )
    finally:
        await file.close()


@app.post("/api/v1/bills/audit", response_model=BillAuditResponse)
def audit_bill_endpoint(request: BillAuditRequest):
    return audit_bill(request)
