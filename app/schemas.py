from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class AuditMetricCreate(BaseModel):
    model_name: str
    risk_level: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    explanations: List[str] = []

    @model_validator(mode="after")
    def validate_explanations(self):
        if self.risk_level == "Crítico" and not self.explanations:
            raise ValueError("Explanations list cannot be empty for 'Crítico' risk level")
        return self

class AuditMetricResponse(AuditMetricCreate):
    id: int
    model_status: str

    class Config:
        from_attributes = True
