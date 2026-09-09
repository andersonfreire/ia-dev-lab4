from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

init_db()

client = TestClient(app)

def test_get_model_status_not_found():
    response = client.get("/api/v1/audit/models/modelo_inexistente/status")
    assert response.status_code == 404
    assert response.json() == {"detail": "Model not found"}