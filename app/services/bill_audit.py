from app.schemas import (
    AuditFinding,
    BillAuditRequest,
    BillAuditResponse,
)

TOLERANCE = 0.02


def audit_bill(request: BillAuditRequest) -> BillAuditResponse:
    findings = []

    for item in request.line_items:
        expected = round(item.quantity * item.unit_price, 2)
        if abs(expected - item.amount) > TOLERANCE:
            findings.append(
                AuditFinding(
                    code="LINE_TOTAL_MISMATCH",
                    message=(
                        f"Check the quantity, unit price, and amount for: "
                        f"{item.description}"
                    ),
                    expected=expected,
                    observed=item.amount,
                )
            )

    expected_total = round(sum(item.amount for item in request.line_items), 2)
    if abs(expected_total - request.stated_total) > TOLERANCE:
        findings.append(
            AuditFinding(
                code="BILL_TOTAL_MISMATCH",
                message=(
                    "The stated total differs from the sum of the supplied "
                    "line amounts."
                ),
                expected=expected_total,
                observed=request.stated_total,
            )
        )

    return BillAuditResponse(
        findings=findings,
        status="review_required" if findings else "checks_passed",
        disclaimer=(
            "Arithmetic checks do not establish medical necessity, incorrect "
            "billing, or fraud. Verify all findings against the original bill "
            "and applicable billing rules."
        ),
    )
