from datetime import datetime

from fastapi import APIRouter, Depends, Query
from starlette import status
from dependencies import getHospitalizacionesService
from schemas.request.AtencionHospitalizaciones_createRequest import AtencionHospitalizaciones_createRequest
from schemas.request.Hospitalizacion_createRequest import Hospitalizacion_createRequest
from schemas.response.AtencionHospitalziacionesResponse import AtencionHospitalziacionesResponse
from schemas.response.AtencionHospitalziacionesDetailResponse import AtencionHospitalziacionesDetailResponse
from schemas.response.GenericResponse import Response
from schemas.response.HospitalizacionResponse import HospitalizacionResponse


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
@router.post("/atencion", response_model=Response[AtencionHospitalziacionesResponse])
def crear_atencion_hospitalizacion(
    data:AtencionHospitalizaciones_createRequest,
    service = Depends(getHospitalizacionesService)
):
    result = service.create_atencion_hospitalizacion(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)


@router.get("/atencion/{id_hospitalizacion}", response_model=Response[list[AtencionHospitalziacionesDetailResponse]])
def obtener_atenciones_hospitalizacion(
    id_hospitalizacion: int,
    id_paciente: int | None = Query(None, title="ID paciente", description="Filtro por id_paciente del triage"),
    id_doctor: int | None = Query(None, title="ID doctor"),
    fecha_inicio: datetime | None = Query(None, title="Fecha inicial de atención"),
    fecha_fin: datetime | None = Query(None, title="Fecha final de atención"),
    id_diagnostico: int | None = Query(None, title="ID diagnóstico"),
    service = Depends(getHospitalizacionesService)
):
    result = service.get_atenciones_por_hospitalizacion(
        id_hospitalizacion=id_hospitalizacion,
        id_paciente=id_paciente,
        id_doctor=id_doctor,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        id_diagnostico=id_diagnostico
    )
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)