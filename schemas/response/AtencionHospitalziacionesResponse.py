from datetime import datetime

from pydantic import BaseModel


class AtencionHospitalziacionesResponse(BaseModel):
    id_atencionh: int
    id_doctor: int
    fecha_atencionh: datetime
    id_diagnostico: int
    id_hospitalizacion: int
    observaciones: str
    tratamiento: str | None
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
