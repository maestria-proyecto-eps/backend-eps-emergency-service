from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from models.Triages import Triages


class TriagesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, triage: Triages):
        self.db.add(triage)

    def get_by_id(self, id_triage: int):
        return (
            self.db.query(Triages)
            .filter(Triages.id_triage == id_triage)
            .first()
        )

    def get_triages(
        self,
        id_paciente: int = None,
        nivel: int = None,
        fecha_inicio: datetime = None,
        fecha_fin: datetime = None,
        estado: int = None,
        riesgo_vital: bool = None,
        pag: int = 1,
        cantidad: int = 30
    ):
        query = self.db.query(Triages)

        if id_paciente is not None:
            query = query.filter(Triages.id_paciente == id_paciente)

        if nivel is not None:
            query = query.filter(Triages.nivel == nivel)

        if estado is not None:
            query = query.filter(Triages.estado == estado)

        if riesgo_vital is not None:
            query = query.filter(Triages.riesgo_vital == riesgo_vital)

        if fecha_inicio is not None:
            query = query.filter(Triages.fechat >= fecha_inicio)

        if fecha_fin is not None:
            query = query.filter(Triages.fechat <= fecha_fin)

        total = query.count()

        data = (
            query
            .order_by(Triages.nivel.desc(), Triages.fechat.asc())
            .offset((pag - 1) * cantidad)
            .limit(cantidad)
            .all()
        )

        return data, total

    def get_first_pending_urgency(self):
        return (
            self.db.query(Triages)
            .filter(Triages.estado == 0)
            .order_by(Triages.nivel.desc(), Triages.fechat.asc())
            .first()
        )