from datetime import datetime

from fastapi import APIRouter, Depends, Query
from starlette import status

from dependencies import getUrgenciasService
from schemas.request.AtencionUrgenciasCreateRequest import AtencionUrgenciasCreateRequest
from schemas.request.TriageCreateRequest import TriageCreateRequest
from schemas.response.AtencionUrgenciasResponse import AtencionUrgenciasResponse
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.GenericResponse import Response
from schemas.response.TriageResponse import TriageResponse
from services.UrgenciasService import UrgenciasService


router = APIRouter(
    prefix="",
    tags=["Urgencias"]
)


@router.post("/triages", response_model=Response[TriageResponse])
def crear_triage(
    data: TriageCreateRequest,
    service: UrgenciasService = Depends(getUrgenciasService)
):
    result = service.crear_triage(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)


@router.get("/triages", response_model=Response[PaginatedResponse[TriageResponse]])
def listar_triages(
    id_paciente: int | None = Query(None),
    nivel: int | None = Query(None),
    fecha_inicio: datetime | None = Query(None),
    fecha_fin: datetime | None = Query(None),
    estado: int | None = Query(None),
    riesgo_vital: bool | None = Query(None),
    pag: int = 1,
    cantidad: int = 30,
    service: UrgenciasService = Depends(getUrgenciasService)
):
    result = service.get_triages(
        id_paciente=id_paciente,
        nivel=nivel,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
        riesgo_vital=riesgo_vital,
        pag=pag,
        cantidad=cantidad
    )
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.get("/triages/urgencia/first", response_model=Response[TriageResponse])
def obtener_primer_triage_pendiente(
    service: UrgenciasService = Depends(getUrgenciasService)
):
    result = service.get_first_pending_urgency()
    if result.hasError:
        return result.toHttpResponse(status.HTTP_404_NOT_FOUND)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.put("/triages/atender/{id_triage}", response_model=Response[TriageResponse])
def atender_triage(
    id_triage: int,
    service: UrgenciasService = Depends(getUrgenciasService)
):
    result = service.atender_triage(id_triage)
    if result.hasError:
        if result.message == "El triage no existe":
            return result.toHttpResponse(status.HTTP_404_NOT_FOUND)
        if result.message == "El triage ya fue atendido":
            return result.toHttpResponse(status.HTTP_409_CONFLICT)
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.post("/atencion_urgencias", response_model=Response[AtencionUrgenciasResponse])
def crear_atencion_urgencias(
    data: AtencionUrgenciasCreateRequest,
    service: UrgenciasService = Depends(getUrgenciasService)
):
    result = service.crear_atencion_urgencias(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)


@router.get("/atencion_urgencias", response_model=Response[PaginatedResponse[AtencionUrgenciasResponse]])
def listar_atenciones_urgencias(
    id_doctor: int | None = Query(None),
    id_paciente: int | None = Query(None),
    fecha_inicio: datetime | None = Query(None),
    fecha_fin: datetime | None = Query(None),
    id_diagnostico: int | None = Query(None),
    pag: int = 1,
    cantidad: int = 30,
    service: UrgenciasService = Depends(getUrgenciasService)
):
    result = service.get_atenciones_urgencias(
        id_doctor=id_doctor,
        id_paciente=id_paciente,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        id_diagnostico=id_diagnostico,
        pag=pag,
        cantidad=cantidad
    )
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)