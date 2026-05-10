from sqlalchemy import Column, DateTime, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class Hospitalizaciones(Base):
    __tablename__ = 'hospitalizaciones'

    id_hospitalizacion = Column(Integer, primary_key=True)
    num_cama = Column(Integer, nullable=True)
    ingreso = Column(DateTime, nullable=True)
    salida = Column(DateTime, nullable=True)
    estado = Column(SmallInteger, nullable=False)
    id_urgencia = Column(Integer, ForeignKey('atencion_urgencias.id_urgencia'), nullable=False)

    urgencia = relationship('AtencionUrgencias', back_populates='hospitalizaciones')

    def __repr__(self):
        return (f"Hospitalizaciones(id_hospitalizacion={self.id_hospitalizacion}, "
                f"num_cama={self.num_cama}, ingreso={self.ingreso}, "
                f"salida={self.salida}, estado={self.estado}, "
                f"id_urgencia={self.id_urgencia})")