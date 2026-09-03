import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Dummy endpoint for testing validation. We will add the actual endpoint later.
from app.schemas import AuditMetricCreate

@app.post("/test/audit")
def mock_audit_endpoint(metric: AuditMetricCreate):
    return {"status": "success"}


def test_validation_rejects_empty_explanations_for_critical():
    payload = {
        "model_name": "credit_scoring",
        "risk_level": "Crítico",
        "confidence_score": 0.85,
        "explanations": []
    }
    response = client.post("/test/audit", json=payload)
    # Task 1.2: should return 400 instead of 422
    assert response.status_code == 400
    assert "Explanations list cannot be empty" in response.text

def test_validation_rejects_score_out_of_bounds_high():
    payload = {
        "model_name": "credit_scoring",
        "risk_level": "Baixo",
        "confidence_score": 1.5,
        "explanations": []
    }
    response = client.post("/test/audit", json=payload)
    assert response.status_code == 400
    assert "Input should be less than or equal to 1" in response.text

def test_validation_rejects_score_out_of_bounds_low():
    payload = {
        "model_name": "credit_scoring",
        "risk_level": "Baixo",
        "confidence_score": -0.1,
        "explanations": []
    }
    response = client.post("/test/audit", json=payload)
    assert response.status_code == 400
    assert "Input should be greater than or equal to 0" in response.text

def test_validation_accepts_valid_payload():
    payload = {
        "model_name": "credit_scoring",
        "risk_level": "Crítico",
        "confidence_score": 0.9,
        "explanations": ["Feature A was high", "Feature B was low"]
    }
    response = client.post("/test/audit", json=payload)
    assert response.status_code == 200
