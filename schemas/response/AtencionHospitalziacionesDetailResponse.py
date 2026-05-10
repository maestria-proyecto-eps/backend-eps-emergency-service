from datetime import datetime

from pydantic import BaseModel


class AtencionHospitalziacionesDetailResponse(BaseModel):
    id_atencionh: int
    id_doctor: int
    fecha_atencionh: datetime
    id_diagnostico: int
    id_hospitalizacion: int
    fecha_atencionh: datetime
    observaciones: str | None
    tratamiento: str | None
    nombre_paciente: str = "No encontrado"
    nombre_doctor: str = "No encontrado"
    nombre_enfermedad: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
