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
from schemas.request.HospitalizacionIngreso_updateRequest import HospitalizacionIngreso_updateRequest
from schemas.response.HospitalizacionDetailResponse import HospitalizacionDetailResponse
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from core.dependencias import RequireRole

router = APIRouter(
    prefix="/hospitalizacion",
    tags=["Hospitalziacion"],
)

@router.post("/", response_model=Response[HospitalizacionResponse], dependencies=[Depends(RequireRole(["Médico"]))])
def crear_hospitalizacion(
    data:Hospitalizacion_createRequest,
    service = Depends(getHospitalizacionesService)
):
    result = service.create_hospitalizacion(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)
@router.post("/atencion", response_model=Response[AtencionHospitalziacionesResponse], dependencies=[Depends(RequireRole(["Médico"]))])
def crear_atencion_hospitalizacion(
    data:AtencionHospitalizaciones_createRequest,
    service = Depends(getHospitalizacionesService)
):
    result = service.create_atencion_hospitalizacion(data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_201_CREATED)


@router.get("/atencion/{id_hospitalizacion}", response_model=Response[list[AtencionHospitalziacionesDetailResponse]], dependencies=[Depends(RequireRole(["Médico"]))])
def obtener_atenciones_hospitalizacion(
    id_hospitalizacion: int,
    id_paciente: int | None = Query(None, title="ID paciente", description="Filtro por id_paciente del triage"),
    id_doctor: int | None = Query(None, title="ID doctor"),
    fecha_inicio: datetime | None = Query(None, title="Fecha inicial de atención"),
    fecha_fin: datetime | None = Query(None, title="Fecha final de atención"),
    id_diagnostico: int | None = Query(None, title="ID diagnóstico"),
    pag: int = 1,
    cantidad: int = 30,
    service = Depends(getHospitalizacionesService)
):
    result = service.get_atenciones_por_hospitalizacion(
        id_hospitalizacion=id_hospitalizacion,
        id_paciente=id_paciente,
        id_doctor=id_doctor,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        id_diagnostico=id_diagnostico,
        pag=pag,
        cantidad=cantidad
    )
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)



@router.put("/ingreso/{id_hospitalizacion}", response_model=Response[HospitalizacionResponse], dependencies=[Depends(RequireRole(["Enfermero"]))])
def registrar_ingreso_hospitalizacion(
    id_hospitalizacion: int,
    data: HospitalizacionIngreso_updateRequest,
    service = Depends(getHospitalizacionesService)
):
    result = service.registrar_ingreso(id_hospitalizacion, data)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.put("/salida/{id_hospitalizacion}", response_model=Response[HospitalizacionResponse], dependencies=[Depends(RequireRole(["Enfermero"]))])
def registrar_salida_hospitalizacion(
    id_hospitalizacion: int,
    service = Depends(getHospitalizacionesService)
):
    result = service.registrar_salida(id_hospitalizacion)
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)


@router.get("/", response_model=Response[PaginatedResponse[HospitalizacionDetailResponse]], dependencies=[Depends(RequireRole(["Enfermero", "Médico"]))])
def listar_hospitalizaciones(
    id_paciente: int | None = Query(None, description="Filtro por id_paciente del triage"),
    num_cama: int | None = Query(None, description="Filtro por número de cama"),
    estado: int | None = Query(None, description="0=no ingresado, 1=ingresado, 2=salido"),
    fecha_ingreso_inicio: datetime | None = Query(None, description="Fecha inicio de ingreso"),
    fecha_ingreso_fin: datetime | None = Query(None, description="Fecha fin de ingreso"),
    fecha_salida_inicio: datetime | None = Query(None, description="Fecha inicio de salida"),
    fecha_salida_fin: datetime | None = Query(None, description="Fecha fin de salida"),
    pag: int = 1,
    cantidad: int = 30,
    service = Depends(getHospitalizacionesService)
):
    result = service.listar_hospitalizaciones(
        id_paciente=id_paciente,
        num_cama=num_cama,
        estado=estado,
        fecha_ingreso_inicio=fecha_ingreso_inicio,
        fecha_ingreso_fin=fecha_ingreso_fin,
        fecha_salida_inicio=fecha_salida_inicio,
        fecha_salida_fin=fecha_salida_fin,
        pag=pag,
        cantidad=cantidad
    )
    if result.hasError:
        return result.toHttpResponse(status.HTTP_400_BAD_REQUEST)
    return result.toHttpResponse(status.HTTP_200_OK)