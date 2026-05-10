from sqlalchemy import Column, BigInteger, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class AtencionHospitalizaciones(Base):
    __tablename__ = 'atencion_hospitalizaciones'

    id_atencionh = Column(Integer, primary_key=True)
    id_doctor = Column(BigInteger, nullable=False)
    fecha_atencionh = Column(DateTime, nullable=False)
    id_diagnostico = Column(Integer, ForeignKey('catalogo_diagnosticos.id_diagnostico'), nullable=False)
    id_hospitalizacion = Column(Integer, ForeignKey('hospitalizaciones.id_hospitalizacion'), nullable=False)
    observaciones = Column(Text, nullable=True)
    tratamiento = Column(Text, nullable=True)

    hospitalizacion = relationship('Hospitalizaciones', back_populates='atencion_hospitalizaciones')
    diagnostico = relationship('CatalogoDiagnosticos', back_populates='atencion_hospitalizaciones')

    @property
    def nombre_enfermedad(self):
        return self.diagnostico.nombre_diagnostico if self.diagnostico else None

    def __repr__(self):
        return (f"AtencionHospitalizaciones(id_atencionh={self.id_atencionh}, id_doctor={self.id_doctor}, "
                f"fecha_atencionh={self.fecha_atencionh}, id_diagnostico={self.id_diagnostico}, "
                f"id_hospitalizacion={self.id_hospitalizacion}, observaciones={self.observaciones}, "
                f"tratamiento={self.tratamiento})")
