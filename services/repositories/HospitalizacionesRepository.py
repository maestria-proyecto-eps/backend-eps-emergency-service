from sqlalchemy.orm import Session

from models.Hospitalizaciones import Hospitalizaciones
from datetime import datetime
from models.AtencionUrgencias import AtencionUrgencias

class HospitalizacionesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, hospitalizacion: Hospitalizaciones):
        self.db.add(hospitalizacion)
        
    def existe_hospitalizacion_por_idurgencia(self, id_urgencia: int) -> bool:
        return self.db.query(Hospitalizaciones).filter(Hospitalizaciones.id_urgencia == id_urgencia).first() is not None
    def existe_hospitalziacion_por_id(self, id_hospitalizacion: int) -> bool:
        return self.db.query(Hospitalizaciones).filter(Hospitalizaciones.id_hospitalizacion == id_hospitalizacion).first() is not None
    
    def get_hospitalizacion_por_id(self, id_hospitalizacion: int):
        return self.db.query(Hospitalizaciones).filter(
            Hospitalizaciones.id_hospitalizacion == id_hospitalizacion
        ).first()

    def get_hospitalizaciones_filtrado(
        self,
        id_paciente: int | None,
        num_cama: int | None,
        estado: int | None,
        fecha_ingreso_inicio: datetime | None,
        fecha_ingreso_fin: datetime | None,
        fecha_salida_inicio: datetime | None,
        fecha_salida_fin: datetime | None,
        pag: int,
        cantidad: int
    ):
        query = self.db.query(Hospitalizaciones)

        if num_cama is not None:
            query = query.filter(Hospitalizaciones.num_cama == num_cama)
        if estado is not None:
            query = query.filter(Hospitalizaciones.estado == estado)
        if fecha_ingreso_inicio:
            query = query.filter(Hospitalizaciones.ingreso >= fecha_ingreso_inicio)
        if fecha_ingreso_fin:
            query = query.filter(Hospitalizaciones.ingreso <= fecha_ingreso_fin)
        if fecha_salida_inicio:
            query = query.filter(Hospitalizaciones.salida >= fecha_salida_inicio)
        if fecha_salida_fin:
            query = query.filter(Hospitalizaciones.salida <= fecha_salida_fin)

        # Filtro por id_paciente: viene del triage/urgencia
        if id_paciente is not None:
            query = query.join(
                Hospitalizaciones.urgencia
            ).filter(
                AtencionUrgencias.id_paciente == id_paciente
            )

        count = query.count()
        data = query.offset((pag - 1) * cantidad).limit(cantidad).all()
        return data, count