from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_bill_total_mismatch():
    response = client.post(
        "/api/v1/bills/audit",
        json={
            "line_items": [
                {"description": "Consultation", "quantity": 1, "unit_price": 500, "amount": 500},
                {"description": "Lab test", "quantity": 2, "unit_price": 250, "amount": 500},
            ],
            "stated_total": 1200,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "review_required"
    assert any(f["code"] == "BILL_TOTAL_MISMATCH" for f in data["findings"])


def test_valid_bill():
    response = client.post(
        "/api/v1/bills/audit",
        json={
            "line_items": [
                {"description": "Consultation", "quantity": 1, "unit_price": 500, "amount": 500}
            ],
            "stated_total": 500,
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "checks_passed"


def test_invalid_quantity_is_rejected():
    response = client.post(
        "/api/v1/bills/audit",
        json={
            "line_items": [
                {"description": "Consultation", "quantity": 0, "unit_price": 500, "amount": 0}
            ],
            "stated_total": 0,
        },
    )
    assert response.status_code == 422
