import datetime

from models.AtencionHospitalizaciones import AtencionHospitalizaciones
from models.Hospitalizaciones import Hospitalizaciones
from schemas.request import AtencionHospitalizaciones_createRequest, Hospitalizacion_createRequest
from schemas.response.AtencionHospitalziacionesResponse import AtencionHospitalziacionesResponse
from schemas.response.HospitalizacionResponse import HospitalizacionResponse
from services.repositories.AtencionHospitalizacionesRepository import AtencionHospitalizacionesRepository
from services.repositories.AtencionUrgenciasRepository import AtencionUrgenciasRepository
from services.repositories.DoctorRepository import DoctorRepository
from services.repositories.DiagnosticoRepository import DiagnosticoRepository
from services.repositories.HospitalizacionesRepository import HospitalizacionesRepository
from schemas.response.GenericResponse import Response


class HospitalizacionesService:
    def __init__(self, repo: HospitalizacionesRepository, repoUrgencias: AtencionUrgenciasRepository,
                  repoDiagnostico: DiagnosticoRepository, repoDoctor: DoctorRepository,
                  repoAtencionHospitalizaciones: AtencionHospitalizacionesRepository):
        self.repo = repo
        self.repoUrgencias = repoUrgencias
        self.repoDiagnostico = repoDiagnostico
        self.repoDoctor = repoDoctor
        self.repoAtencionHospitalizaciones = repoAtencionHospitalizaciones

    def create_hospitalizacion(self, request: Hospitalizacion_createRequest):
        if not self.repoUrgencias.existe_atencion_urgencia_por_id(request.id_urgencia):
            return Response.error("La atención de urgencias no existe")
        if self.repo.existe_hospitalizacion_por_idurgencia(request.id_urgencia):
            return Response.error("Ya existe una hospitalización para esta atención de urgencias")
        nueva_hospitalizacion = Hospitalizaciones(
            num_cama=None,
            ingreso=None,
            salida=None,
            estado=0,
            id_urgencia=request.id_urgencia
        )
        self.repo.add(nueva_hospitalizacion)
        self.repo.db.commit()
        self.repo.db.refresh(nueva_hospitalizacion)
        return Response.ok(HospitalizacionResponse.model_validate(nueva_hospitalizacion), "Hospitalización creada exitosamente")
    def create_atencion_hospitalizacion(self, request: AtencionHospitalizaciones_createRequest):
        if(not self.repoDoctor.existe_doctor(request.id_doctor)):
            return Response.error("El doctor no existe")
        if(not self.repoDiagnostico.existe_diagnostico_por_id(request.id_diagnostico)):
            return Response.error("El diagnóstico no existe")
        if(not self.repo.existe_hospitalziacion_por_id(request.id_hospitalizacion)):
            return Response.error("La hospitalización no existe")
        atencion = AtencionHospitalizaciones(**request.model_dump())
        atencion.fecha_atencionh = datetime.datetime.now()
        self.repoAtencionHospitalizaciones.add(atencion)
        self.repo.db.commit()
        self.repo.db.refresh(atencion)
        return Response.ok(AtencionHospitalziacionesResponse.model_validate(atencion), "Atención creada exitosamente")
