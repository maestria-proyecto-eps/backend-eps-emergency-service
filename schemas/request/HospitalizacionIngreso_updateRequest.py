from pydantic import BaseModel

class HospitalizacionIngreso_updateRequest(BaseModel):
    num_cama: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }