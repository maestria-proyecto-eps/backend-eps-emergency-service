import datetime
import math

from models.AtencionHospitalizaciones import AtencionHospitalizaciones
from models.Hospitalizaciones import Hospitalizaciones
from schemas.request import AtencionHospitalizaciones_createRequest, Hospitalizacion_createRequest
from schemas.response.AtencionHospitalziacionesResponse import AtencionHospitalziacionesResponse
from schemas.response.AtencionHospitalziacionesDetailResponse import AtencionHospitalziacionesDetailResponse
from schemas.response.GenericPaginatedResponse import PaginatedResponse
from schemas.response.HospitalizacionResponse import HospitalizacionResponse
from services.repositories.PersonaRepository import PersonaRepository
from services.repositories.AtencionHospitalizacionesRepository import AtencionHospitalizacionesRepository
from services.repositories.AtencionUrgenciasRepository import AtencionUrgenciasRepository
from services.repositories.DoctorRepository import DoctorRepository
from services.repositories.DiagnosticoRepository import DiagnosticoRepository
from services.repositories.HospitalizacionesRepository import HospitalizacionesRepository
from schemas.response.GenericResponse import Response
from schemas.request.HospitalizacionIngreso_updateRequest import HospitalizacionIngreso_updateRequest
from schemas.response.HospitalizacionDetailResponse import HospitalizacionDetailResponse

class HospitalizacionesService:
    def __init__(self, repo: HospitalizacionesRepository, repoUrgencias: AtencionUrgenciasRepository,
                  repoDiagnostico: DiagnosticoRepository, repoDoctor: DoctorRepository,
                  repoAtencionHospitalizaciones: AtencionHospitalizacionesRepository,
                  repoPersona: PersonaRepository):
        self.repo = repo
        self.repoUrgencias = repoUrgencias
        self.repoDiagnostico = repoDiagnostico
        self.repoDoctor = repoDoctor
        self.repoAtencionHospitalizaciones = repoAtencionHospitalizaciones
        self.repoPersona = repoPersona

    def get_atenciones_por_hospitalizacion(self,
                                           id_hospitalizacion: int,
                                           id_paciente: int | None = None,
                                           id_doctor: int | None = None,
                                           fecha_inicio = None,
                                           fecha_fin = None,
                                           id_diagnostico: int | None = None,
                                           pag:int=1, cantidad: int=10):
        if not self.repo.existe_hospitalziacion_por_id(id_hospitalizacion):
            return Response.error("La hospitalización no existe")
        
        id_paciente = self.repoUrgencias.get_id_paciente_por_atencion_urgencia(id_hospitalizacion)
        nombrePaciente = "No encontrado"
        if id_paciente:
            persona = self.repoPersona.get_persona_por_id(id_paciente)
            if persona:
                nombrePaciente = persona.nombres + " " + persona.apellidos
        data, count = self.repoAtencionHospitalizaciones.get_by_hospitalizacion(
            id_hospitalizacion=id_hospitalizacion,
            id_paciente=id_paciente,
            id_doctor=id_doctor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_diagnostico=id_diagnostico,
            pag=pag,
            cantidad=cantidad
        )
        totalPags = math.ceil(count / cantidad)
        response = [AtencionHospitalziacionesDetailResponse.model_validate(e) for e in data]
        for r in response:
            doctor = self.repoPersona.get_persona_por_id(r.id_doctor)
            if doctor:
                r.nombre_doctor = doctor.nombres + " " + doctor.apellidos
            r.nombre_paciente = nombrePaciente
        return Response.ok(PaginatedResponse[AtencionHospitalziacionesDetailResponse](
            data=response, 
            page=pag, 
            pages=totalPags
        ), "Listado de atenciones de hospitalización")

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

    def registrar_ingreso(self, id_hospitalizacion: int, request: HospitalizacionIngreso_updateRequest):
        hosp = self.repo.get_hospitalizacion_por_id(id_hospitalizacion)
        
        if not hosp:
            return Response.error("La hospitalización no existe")
        if int(hosp.estado) != 0:
            return Response.error("La hospitalización ya fue ingresada o dada de salida")

        hosp.num_cama = request.num_cama
        hosp.ingreso = datetime.datetime.now()
        hosp.estado = 1
        self.repo.db.commit()
        self.repo.db.refresh(hosp)
        return Response.ok(HospitalizacionResponse.model_validate(hosp), "Ingreso registrado exitosamente")


    def registrar_salida(self, id_hospitalizacion: int):
        hosp = self.repo.get_hospitalizacion_por_id(id_hospitalizacion)
        if not hosp:
            return Response.error("La hospitalización no existe")
        if int(hosp.estado) != 1:
            return Response.error("La hospitalización no está en estado ingresado")

        hosp.salida = datetime.datetime.now()
        hosp.estado = 2
        self.repo.db.commit()
        self.repo.db.refresh(hosp)
        return Response.ok(HospitalizacionResponse.model_validate(hosp), "Salida registrada exitosamente")


    def listar_hospitalizaciones(
        self,
        id_paciente: int | None,
        num_cama: int | None,
        estado: int | None,
        fecha_ingreso_inicio,
        fecha_ingreso_fin,
        fecha_salida_inicio,
        fecha_salida_fin,
        pag: int,
        cantidad: int
    ):
        data, count = self.repo.get_hospitalizaciones_filtrado(
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
        totalPags = math.ceil(count / cantidad) if cantidad else 1
        response = []
        for hosp in data:
            item = HospitalizacionDetailResponse.model_validate(hosp)
            id_pac = self.repoUrgencias.get_id_paciente_por_atencion_urgencia(hosp.id_urgencia)
            item.id_paciente = id_pac
            if id_pac:
                persona = self.repoPersona.get_persona_por_id(id_pac)
                if persona:
                    item.nombre_paciente = persona.nombres + " " + persona.apellidos
            response.append(item)

        return Response.ok(PaginatedResponse[HospitalizacionDetailResponse](
            data=response,
            page=pag,
            pages=totalPags
        ), "Listado de hospitalizaciones")