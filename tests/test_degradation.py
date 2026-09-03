import pytest
import logging
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal, AuditMetric
from app.services import save_audit_metric, check_model_degradation
from app.schemas import AuditMetricCreate

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_degradation_blocks_model_and_logs_critical(caplog):
    db = SessionLocal()
    
    # Insert 50 metrics with average < 0.70
    # Let's say 25 with 1.0 and 25 with 0.3 => avg = 0.65
    for i in range(25):
        save_audit_metric(db, AuditMetricCreate(
            model_name="test_model", risk_level="Alto", confidence_score=1.0, explanations=[]
        ))
    for i in range(25):
        save_audit_metric(db, AuditMetricCreate(
            model_name="test_model", risk_level="Alto", confidence_score=0.3, explanations=[]
        ))
    
    # check_model_degradation is called internally inside save_audit_metric
    
    # Assert model is blocked
    latest = db.query(AuditMetric).filter(AuditMetric.model_name == "test_model").order_by(AuditMetric.id.desc()).first()
    assert latest is not None
    assert str(latest.model_status) == "BLOCKED"
    
    # Now intercept via prediction
    with caplog.at_level(logging.CRITICAL):
        response = client.post("/api/v1/predict/test_model", json={"data": 123})
        
    assert response.status_code == 403
    assert response.json()["detail"] == "Model is blocked"
    
    # Check log
    assert "Prediction rejected: Model 'test_model' is BLOCKED due to degradation." in caplog.text
    
    db.close()

def test_degradation_does_not_block_model_if_average_is_high():
    db = SessionLocal()
    
    # Insert 50 metrics with average >= 0.70
    # 50 with 0.8 => avg = 0.8
    for i in range(50):
        save_audit_metric(db, AuditMetricCreate(
            model_name="test_model_good", risk_level="Baixo", confidence_score=0.8, explanations=[]
        ))
        
    latest = db.query(AuditMetric).filter(AuditMetric.model_name == "test_model_good").order_by(AuditMetric.id.desc()).first()
    assert latest is not None
    assert str(latest.model_status) == "ACTIVE"
    
    response = client.post("/api/v1/predict/test_model_good", json={"data": 123})
    assert response.status_code == 200
    
    db.close()
