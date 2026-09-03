import json
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./audit.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AuditMetric(Base):
    __tablename__ = "audit_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    risk_level = Column(String)
    confidence_score = Column(Float)
    explanations = Column(Text)  # Stored as JSON string
    model_status = Column(String, default="ACTIVE")

# Helper functions to convert list to JSON string and vice versa
def get_explanations(metric: AuditMetric) -> list:
    if metric.explanations is not None and str(metric.explanations) != "":
        return json.loads(str(metric.explanations))
    return []

def set_explanations(metric: AuditMetric, explanations: list):
    metric.explanations = json.dumps(explanations)  # type: ignore

def init_db():
    Base.metadata.create_all(bind=engine)
