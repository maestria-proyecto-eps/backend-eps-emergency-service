from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base


class CatalogoDiagnosticos(Base):
    __tablename__ = 'catalogo_diagnosticos'

    id_diagnostico = Column(Integer, primary_key=True)
    nombre_enfermedad = Column(String(50), nullable=False)

    atencion_hospitalizaciones = relationship('AtencionHospitalizaciones', back_populates='diagnostico')
    atenciones_urgencias = relationship('AtencionUrgencias', back_populates='diagnostico')

    def __repr__(self):
        return f"CatalogoDiagnosticos(id_diagnostico={self.id_diagnostico}, nombre_enfermedad={self.nombre_enfermedad})"
