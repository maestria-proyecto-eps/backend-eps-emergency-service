from sqlalchemy.orm import Session

from models.AtencionHospitalizaciones import AtencionHospitalizaciones


class AtencionHospitalizacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, hospitalizacion: AtencionHospitalizaciones):
        self.db.add(hospitalizacion)
        