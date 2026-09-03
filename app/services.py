import logging
from sqlalchemy.orm import Session
# Adicionada a configuração do logger
logger = logging.getLogger(__name__)
from .schemas import AuditMetricCreate
from .database import AuditMetric, set_explanations

def save_audit_metric(db: Session, metric_in: AuditMetricCreate):
    db_metric = AuditMetric(
        model_name=metric_in.model_name,
        risk_level=metric_in.risk_level,
        confidence_score=metric_in.confidence_score,
        model_status="ACTIVE"
    )
    set_explanations(db_metric, metric_in.explanations)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    
    check_model_degradation(db, metric_in.model_name)
    return db_metric

def check_model_degradation(db: Session, model_name: str):
    # Fetch the last 50 predictions for the model
    recent_metrics = db.query(AuditMetric).filter(
        AuditMetric.model_name == model_name
    ).order_by(AuditMetric.id.desc()).limit(50).all()
    
    if len(recent_metrics) > 0:
        avg_score = sum(m.confidence_score for m in recent_metrics) / len(recent_metrics)
        
        # If the average is below 0.70, update all active metrics to BLOCKED for this model
        if avg_score < 0.70:
            db.query(AuditMetric).filter(
                AuditMetric.model_name == model_name,
                AuditMetric.model_status == "ACTIVE"
            ).update({"model_status": "BLOCKED"})
            db.commit()
            
            # Emissão do alerta movida para o momento exato do bloqueio assíncrono
            logger.critical(f"ALERTA DE GOVERNANÇA: O modelo '{model_name}' foi BLOQUEADO. Confiança média degradada para {avg_score:.2f}.")
            return True
    return False
