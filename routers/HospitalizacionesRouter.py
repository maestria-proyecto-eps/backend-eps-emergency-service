from fastapi import APIRouter, Depends
from starlette import status
from dependencies import getHospitalizacionesService
from schemas.request.Hospitalizacion_createRequest import Hospitalizacion_createRequest
from schemas.response.GenericResponse import Response
from schemas.response.HospitalizacionResponse import HospitalizacionResponse
from services.HospitalizacionesService import HospitalizacionesService


router = APIRouter(
    prefix="/hospitalizacion",
    tags=["Hospitalziacion"],
)

@router.post("/", response_model=Response[HospitalizacionResponse])
def crear_hospitalizacion(
    data:Hospitalizacion_createRequest,
    service = Depends(getHospitalizacionesService)
):
    result = service.create_hospitalizacion(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)