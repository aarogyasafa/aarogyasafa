from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app: str


class DocumentAnalysis(BaseModel):
    filename: str
    extracted_text: str
    status: str
    message: str


class BillLineItem(BaseModel):
    description: str = Field(min_length=1, max_length=500)
    quantity: float = Field(gt=0, le=1_000_000)
    unit_price: float = Field(ge=0, le=1_000_000_000)
    amount: float = Field(ge=0, le=1_000_000_000)


class BillAuditRequest(BaseModel):
    line_items: list[BillLineItem] = Field(min_length=1, max_length=5000)
    stated_total: float = Field(ge=0, le=1_000_000_000)


class AuditFinding(BaseModel):
    code: str
    message: str
    expected: float
    observed: float


class BillAuditResponse(BaseModel):
    findings: list[AuditFinding]
    status: str
    disclaimer: str
