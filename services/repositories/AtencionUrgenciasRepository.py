from sqlalchemy.orm import Session

from models.AtencionUrgencias import AtencionUrgencias


class AtencionUrgenciasRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_atencion_urgencia_por_id(self, idAtencionUrgencia: int) -> bool:
        return self.db.query(AtencionUrgencias).filter(AtencionUrgencias.id_urgencia == idAtencionUrgencia).first() is not None