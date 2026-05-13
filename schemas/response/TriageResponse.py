from datetime import datetime
from pydantic import BaseModel


class TriageResponse(BaseModel):
    id_triage: int
    id_paciente: int
    motivo: str
    nivel: int
    id_enfermero: int
    antecedentes: str | None = None
    fechat: datetime
    estado: int
    alergias: str | None = None
    hallazgos: str
    medicamentos: str | None = None
    pulso: str | None = None
    presion_arterial: str | None = None
    frecuencia_cardiaca: str | None = None
    frecuencia_respiratoria: str | None = None
    temperatura: str | None = None
    saturacion_oxigeno: str | None = None
    escala_dolor: int | None = None
    riesgo_vital: bool

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }