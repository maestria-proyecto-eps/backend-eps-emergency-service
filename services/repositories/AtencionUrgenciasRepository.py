from sqlalchemy.orm import Session, joinedload

from models.AtencionUrgencias import AtencionUrgencias


class AtencionUrgenciasRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_atencion_urgencia_por_id(self, idAtencionUrgencia: int) -> bool:
        return self.db.query(AtencionUrgencias).filter(AtencionUrgencias.id_urgencia == idAtencionUrgencia).first() is not None
    def get_id_paciente_por_atencion_urgencia(self, idAtencionUrgencia: int) -> int | None:
        atencion = self.db.query(AtencionUrgencias).options(joinedload(AtencionUrgencias.triage)).filter(AtencionUrgencias.id_urgencia == idAtencionUrgencia).first()
        if atencion:
            return atencion.triage.id_paciente
        return None