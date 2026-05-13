from sqlalchemy.orm import Session, joinedload

from models.AtencionUrgencias import AtencionUrgencias
from models.Triages import Triages


class AtencionUrgenciasRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_atencion_urgencia_por_id(self, idAtencionUrgencia: int) -> bool:
        return (
            self.db.query(AtencionUrgencias)
            .filter(AtencionUrgencias.id_urgencia == idAtencionUrgencia)
            .first()
            is not None
        )

    def get_id_paciente_por_atencion_urgencia(self, idAtencionUrgencia: int) -> int | None:
        atencion = self.db.query(AtencionUrgencias).options(joinedload(AtencionUrgencias.triage)).filter(AtencionUrgencias.id_urgencia == idAtencionUrgencia).first()
        if atencion and atencion.triage:
            return atencion.triage.id_paciente
        return None

    def add(self, atencion: AtencionUrgencias):
        self.db.add(atencion)

    def get_atenciones_urgencias(
        self,
        id_doctor: int = None,
        id_paciente: int = None,
        fecha_inicio=None,
        fecha_fin=None,
        id_diagnostico: int = None,
        pag: int = 1,
        cantidad: int = 30
    ):
        query = (
            self.db.query(AtencionUrgencias)
            .join(Triages, AtencionUrgencias.id_triage == Triages.id_triage)
            .options(joinedload(AtencionUrgencias.triage))
        )

        if id_doctor is not None:
            query = query.filter(AtencionUrgencias.id_doctor == id_doctor)

        if id_paciente is not None:
            query = query.filter(Triages.id_paciente == id_paciente)

        if id_diagnostico is not None:
            query = query.filter(AtencionUrgencias.id_diagnostico == id_diagnostico)

        if fecha_inicio is not None:
            query = query.filter(Triages.fechat >= fecha_inicio)

        if fecha_fin is not None:
            query = query.filter(Triages.fechat <= fecha_fin)

        total = query.count()

        data = (
            query
            .order_by(AtencionUrgencias.id_urgencia.asc())
            .offset((pag - 1) * cantidad)
            .limit(cantidad)
            .all()
        )

        return data, total