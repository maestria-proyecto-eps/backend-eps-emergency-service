from sqlalchemy.orm import Session

from models.CatalogoDiagnosticos import CatalogoDiagnosticos
from models.AtencionHospitalizaciones import AtencionHospitalizaciones
from models.Hospitalizaciones import Hospitalizaciones
from models.AtencionUrgencias import AtencionUrgencias
from models.Triages import Triages


class AtencionHospitalizacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, hospitalizacion: AtencionHospitalizaciones):
        self.db.add(hospitalizacion)

    def get_by_hospitalizacion(self,
                               id_hospitalizacion: int,
                               id_paciente: int | None = None,
                               id_doctor: int | None = None,
                               fecha_inicio = None,
                               fecha_fin = None,
                               id_diagnostico: int | None = None,
                               pag:int=1, cantidad: int=10):
        query = self.db.query(AtencionHospitalizaciones)
        query = query.join(Hospitalizaciones, AtencionHospitalizaciones.hospitalizacion)
        query = query.join(AtencionUrgencias, Hospitalizaciones.urgencia)
        query = query.join(CatalogoDiagnosticos, AtencionUrgencias.diagnostico)
        query = query.join(Triages, AtencionUrgencias.triage)
        query = query.filter(AtencionHospitalizaciones.id_hospitalizacion == id_hospitalizacion)

        if id_paciente is not None:
            query = query.filter(Triages.id_paciente == id_paciente)
        if id_doctor is not None:
            query = query.filter(AtencionHospitalizaciones.id_doctor == id_doctor)
        if id_diagnostico is not None:
            query = query.filter(AtencionHospitalizaciones.id_diagnostico == id_diagnostico)
        if fecha_inicio is not None:
            query = query.filter(AtencionHospitalizaciones.fecha_atencionh >= fecha_inicio)
        if fecha_fin is not None:
            query = query.filter(AtencionHospitalizaciones.fecha_atencionh <= fecha_fin)

        count_smt = query.count()
        offset = (pag - 1) * cantidad
        query = (
            query
            .offset(offset)
            .limit(cantidad)
        )
        result = self.db.execute(query)
        results = result.scalars().all()
        return results, count_smt
        
