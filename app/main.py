from fastapi import FastAPI, Request, status, Depends, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .database import init_db, SessionLocal
from .schemas import AuditMetricCreate
from .services import save_audit_metric

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Audit API", version="1.0.0", lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Task 1.2: Sobrescrever tratador de exceção
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": jsonable_encoder(exc.errors())},
    )

def background_save_metric(metric_in: AuditMetricCreate):
    db = SessionLocal()
    try:
        save_audit_metric(db, metric_in)
    finally:
        db.close()

# Task 2.1: Rota de ingestão assíncrona
@app.post("/api/v1/audit/metrics", status_code=status.HTTP_201_CREATED)
def create_audit_metric(metric: AuditMetricCreate, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_save_metric, metric)
    return {"message": "Metric received for processing"}



import logging
from fastapi import HTTPException
from .database import AuditMetric

logger = logging.getLogger(__name__)

@app.post("/api/v1/predict/{model_name}")
def predict(model_name: str, payload: dict, db: Session = Depends(get_db)):
    # Check if the model is blocked
    # We query to see if there is any metric with status BLOCKED for this model
    # To optimize, we can just check the latest status
    latest_metric = db.query(AuditMetric).filter(
        AuditMetric.model_name == model_name
    ).order_by(AuditMetric.id.desc()).first()

    if latest_metric is not None and str(latest_metric.model_status) == "BLOCKED":
        logger.critical(f"Prediction rejected: Model '{model_name}' is BLOCKED due to degradation.")
        raise HTTPException(status_code=403, detail="Model is blocked")
    
    return {"prediction": "success", "model_name": model_name}

@app.get("/health")
def health_check():
    return {"status": "ok"}
