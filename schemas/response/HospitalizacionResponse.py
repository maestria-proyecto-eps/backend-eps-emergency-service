from datetime import datetime

from pydantic import BaseModel


class HospitalizacionResponse(BaseModel):
    id_hospitalizacion :int
    num_cama :int | None
    ingreso :datetime | None
    salida :datetime | None
    estado :int
    id_urgencia :int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }