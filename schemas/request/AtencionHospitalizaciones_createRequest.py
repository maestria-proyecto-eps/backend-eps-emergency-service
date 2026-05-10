from pydantic import BaseModel


class AtencionHospitalizaciones_createRequest(BaseModel):
    id_doctor: int
    id_diagnostico: int
    id_hospitalizacion: int
    observaciones: str
    tratamiento: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }