from sqlalchemy import Column, Integer, BigInteger
from db.session import  BaseAdmin


class Doctor(BaseAdmin):
    __tablename__ = "medicos"

    id_medico = Column(BigInteger, primary_key=True)
    num_licencia = Column(Integer, unique=True, nullable=False)
    id_especialidad = Column(Integer, nullable=False)
