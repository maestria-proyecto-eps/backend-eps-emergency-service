from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, SmallInteger, String, Text
from sqlalchemy.orm import relationship

from db.session import Base


class Triages(Base):
    __tablename__ = 'triages'

    id_triage = Column(Integer, primary_key=True)
    id_paciente = Column(BigInteger, nullable=False)
    motivo = Column(String(100), nullable=False)
    nivel = Column(SmallInteger, nullable=False)
    id_enfermero = Column(Integer, nullable=False)
    antecedentes = Column(String(200), nullable=True)
    fechat = Column(DateTime, nullable=False)
    estado = Column(SmallInteger, nullable=False)
    alergias = Column(String(100), nullable=True)
    hallazgos = Column(Text, nullable=False)
    medicamentos = Column(String(300), nullable=True)
    pulso = Column(String(50), nullable=True)
    presion_arterial = Column(String(50), nullable=True)
    frecuencia_cardiaca = Column(String(50), nullable=True)
    frecuencia_respiratoria = Column(String(50), nullable=True)
    temperatura = Column(String(50), nullable=True)
    saturacion_oxigeno = Column(String(50), nullable=True)
    escala_dolor = Column(SmallInteger, nullable=True)
    riesgo_vital = Column(Boolean, nullable=False)

    atencion_urgencias = relationship('AtencionUrgencias', back_populates='triage')

    def __repr__(self):
        return (f"Triages(id_triage={self.id_triage}, id_paciente={self.id_paciente}, motivo={self.motivo}, "
                f"nivel={self.nivel}, id_enfermero={self.id_enfermero}, antecedentes={self.antecedentes}, "
                f"fechaT={self.fechaT}, estado={self.estado}, alergias={self.alergias}, "
                f"hallazgos={self.hallazgos}, medicamentos={self.medicamentos}, pulso={self.pulso}, "
                f"presion_arterial={self.presion_arterial}, frecuencia_cardiaca={self.frecuencia_cardiaca}, "
                f"frecuencia_respiratoria={self.frecuencia_respiratoria}, temperatura={self.temperatura}, "
                f"saturacion_oxigeno={self.saturacion_oxigeno}, escala_dolor={self.escala_dolor}, "
                f"riesgo_vital={self.riesgo_vital})")
