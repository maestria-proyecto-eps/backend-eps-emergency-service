from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class AtencionUrgencias(Base):
    __tablename__ = 'atencion_urgencias'

    id_urgencia = Column(Integer, primary_key=True)
    id_doctor = Column(BigInteger, nullable=False)
    observaciones = Column(Text, nullable=True)
    tratamiento = Column(Text, nullable=True)
    id_triage = Column(Integer, ForeignKey('triages.id_triage'), nullable=False)
    id_diagnostico = Column(Integer, ForeignKey('catalogo_diagnosticos.id_diagnostico'), nullable=False)

    triage = relationship('Triages', back_populates='atencion_urgencias')
    diagnostico = relationship('CatalogoDiagnosticos', back_populates='atenciones_urgencias')
    hospitalizaciones = relationship('Hospitalizaciones', back_populates='urgencia')

    def __repr__(self):
        return (f"AtencionUrgencias(id_urgencia={self.id_urgencia}, id_doctor={self.id_doctor}, "
                f"observaciones={self.observaciones}, tratamiento={self.tratamiento}, "
                f"id_triage={self.id_triage}, id_diagnostico={self.id_diagnostico})")

