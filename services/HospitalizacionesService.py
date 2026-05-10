from models.Hospitalizaciones import Hospitalizaciones
from schemas.request import Hospitalizacion_createRequest
from schemas.response.HospitalizacionResponse import HospitalizacionResponse
from services.repositories import AtencionUrgenciasRepository
from services.repositories.HospitalizacionesRepository import HospitalizacionesRepository
from schemas.response.GenericResponse import Response


class HospitalizacionesService:
    def __init__(self, repo: HospitalizacionesRepository, repoUrgencias: AtencionUrgenciasRepository):
        self.repo = repo
        self.repoUrgencias = repoUrgencias

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