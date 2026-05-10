from sqlalchemy.orm import Session

from models.Hospitalizaciones import Hospitalizaciones


class HospitalizacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, hospitalizacion: Hospitalizaciones):
        self.db.add(hospitalizacion)
        
    def existe_hospitalizacion_por_idurgencia(self, id_urgencia: int) -> bool:
        return self.db.query(Hospitalizaciones).filter(Hospitalizaciones.id_urgencia == id_urgencia).first() is not None