from db import session
from models.CatalogoDiagnosticos import CatalogoDiagnosticos


class DiagnosticoRepository:
    def __init__(self, db:session):
        self.db = db

    def existe_diagnostico_por_id(self, idDiagnostico: int) -> bool:
        return self.db.query(CatalogoDiagnosticos).filter(CatalogoDiagnosticos.id_diagnostico == idDiagnostico).first() is not None