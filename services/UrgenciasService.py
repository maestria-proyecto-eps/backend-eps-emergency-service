import math
from datetime import datetime

from models.AtencionUrgencias import AtencionUrgencias
from models.Triages import Triages
from schemas.request.AtencionUrgenciasCreateRequest import AtencionUrgenciasCreateRequest
from schemas.request.TriageCreateRequest import TriageCreateRequest
from schemas.response.AtencionUrgenciasResponse import AtencionUrgenciasResponse
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.GenericResponse import Response
from schemas.response.TriageResponse import TriageResponse
from services.repositories.AtencionUrgenciasRepository import AtencionUrgenciasRepository
from services.repositories.DiagnosticoRepository import DiagnosticoRepository
from services.repositories.DoctorRepository import DoctorRepository
from services.repositories.TriagesRepository import TriagesRepository


class UrgenciasService:
    def __init__(
        self,
        repo_triages: TriagesRepository,
        repo_atencion_urgencias: AtencionUrgenciasRepository,
        repo_doctor: DoctorRepository,
        repo_diagnostico: DiagnosticoRepository
    ):
        self.repo_triages = repo_triages
        self.repo_atencion_urgencias = repo_atencion_urgencias
        self.repo_doctor = repo_doctor
        self.repo_diagnostico = repo_diagnostico

    def crear_triage(self, request: TriageCreateRequest):
        triage = Triages(**request.model_dump())
        triage.estado = 0
        triage.fechat = datetime.now()

        self.repo_triages.add(triage)
        self.repo_triages.db.commit()
        self.repo_triages.db.refresh(triage)

        return Response.ok(
            TriageResponse.model_validate(triage),
            "Triage creado exitosamente"
        )

    def get_triages(
        self,
        id_paciente: int = None,
        nivel: int = None,
        fecha_inicio=None,
        fecha_fin=None,
        estado: int = None,
        riesgo_vital: bool = None,
        pag: int = 1,
        cantidad: int = 30
    ):
        data, total = self.repo_triages.get_triages(
            id_paciente=id_paciente,
            nivel=nivel,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
            riesgo_vital=riesgo_vital,
            pag=pag,
            cantidad=cantidad
        )

        total_pags = math.ceil(total / cantidad) if total > 0 else 0

        response = [TriageResponse.model_validate(t) for t in data]

        return Response.ok(
            PaginatedResponse[TriageResponse](
                data=response,
                page=pag,
                pages=total_pags
            ),
            "Listado de triages"
        )

    def get_first_pending_urgency(self):
        triage = self.repo_triages.get_first_pending_urgency()

        if triage is None:
            return Response.error("No hay triages pendientes")

        return Response.ok(
            TriageResponse.model_validate(triage),
            "Primer triage pendiente obtenido exitosamente"
        )

    def atender_triage(self, id_triage: int):
        triage = self.repo_triages.get_by_id(id_triage)

        if triage is None:
            return Response.error("El triage no existe")

        if triage.estado == 1:
            return Response.error("El triage ya fue atendido")

        triage.estado = 1
        self.repo_triages.db.commit()
        self.repo_triages.db.refresh(triage)

        return Response.ok(
            TriageResponse.model_validate(triage),
            "Triage atendido exitosamente"
        )

    def crear_atencion_urgencias(self, request: AtencionUrgenciasCreateRequest):
        triage = self.repo_triages.get_by_id(request.id_triage)

        if triage is None:
            return Response.error("El triage no existe")

        if not self.repo_doctor.existe_doctor(request.id_doctor):
            return Response.error("El doctor no existe")

        if not self.repo_diagnostico.existe_diagnostico_por_id(request.id_diagnostico):
            return Response.error("El diagnóstico no existe")

        atencion = AtencionUrgencias(**request.model_dump())

        self.repo_atencion_urgencias.add(atencion)
        self.repo_atencion_urgencias.db.commit()
        self.repo_atencion_urgencias.db.refresh(atencion)

        return Response.ok(
            AtencionUrgenciasResponse.model_validate(atencion),
            "Atención de urgencias creada exitosamente"
        )

    def get_atenciones_urgencias(
        self,
        id_doctor: int = None,
        id_paciente: int = None,
        fecha_inicio=None,
        fecha_fin=None,
        id_diagnostico: int = None,
        pag: int = 1,
        cantidad: int = 30
    ):
        data, total = self.repo_atencion_urgencias.get_atenciones_urgencias(
            id_doctor=id_doctor,
            id_paciente=id_paciente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_diagnostico=id_diagnostico,
            pag=pag,
            cantidad=cantidad
        )

        total_pags = math.ceil(total / cantidad) if total > 0 else 0

        response = [AtencionUrgenciasResponse.model_validate(a) for a in data]

        return Response.ok(
            PaginatedResponse[AtencionUrgenciasResponse](
                data=response,
                page=pag,
                pages=total_pags
            ),
            "Listado de atenciones de urgencias"
        )