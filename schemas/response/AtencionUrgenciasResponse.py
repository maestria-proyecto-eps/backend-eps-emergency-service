from pydantic import BaseModel


class AtencionUrgenciasResponse(BaseModel):
    id_urgencia: int
    id_doctor: int
    observaciones: str | None = None
    tratamiento: str | None = None
    id_triage: int
    id_diagnostico: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }