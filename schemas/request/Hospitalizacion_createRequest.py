from pydantic import BaseModel


class Hospitalizacion_createRequest(BaseModel):
    id_urgencia: int
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }