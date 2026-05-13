#Repositories
from fastapi import Depends

from db.session import get_db, get_db_admin
from services.HospitalizacionesService import HospitalizacionesService
from services.repositories.AtencionHospitalizacionesRepository import AtencionHospitalizacionesRepository
from services.repositories.DiagnosticoRepository import DiagnosticoRepository
from services.repositories.DoctorRepository import DoctorRepository
from services.repositories.HospitalizacionesRepository import HospitalizacionesRepository
from services.repositories.AtencionUrgenciasRepository import AtencionUrgenciasRepository
from services.repositories.PersonaRepository import PersonaRepository
from services.UrgenciasService import UrgenciasService
from services.repositories.TriagesRepository import TriagesRepository

#Repositories
def getAtencionUrgenciasRepository(db = Depends(get_db))-> AtencionUrgenciasRepository:
    return AtencionUrgenciasRepository(db)
def getHospitalizacionesRepository(db = Depends(get_db))-> HospitalizacionesRepository:
    return HospitalizacionesRepository(db)
def getDiagnosticosRepository(db = Depends(get_db))-> DiagnosticoRepository:
    return DiagnosticoRepository(db)
def getDoctorRepository(db = Depends(get_db_admin))-> DoctorRepository:
    return DoctorRepository(db)
def getAtencionHospitalizacionesRepository(db = Depends(get_db))-> AtencionHospitalizacionesRepository:
    return AtencionHospitalizacionesRepository(db)
def getPersonaRepository(db = Depends(get_db_admin))-> PersonaRepository:
    return PersonaRepository(db)
def getTriagesRepository(db = Depends(get_db)) -> TriagesRepository:
    return TriagesRepository(db)
#Services
def getHospitalizacionesService(
    hospitalizacionesRepository: HospitalizacionesRepository = Depends(getHospitalizacionesRepository),
    atencionUrgenciasRepository: AtencionUrgenciasRepository = Depends(getAtencionUrgenciasRepository),
    repoAtencionHospitalizaciones: AtencionHospitalizacionesRepository = Depends(getAtencionHospitalizacionesRepository),
    repoDiagnostico: DiagnosticoRepository = Depends(getDiagnosticosRepository),
    repoDoctor: DoctorRepository = Depends(getDoctorRepository),
    repoPersona: PersonaRepository = Depends(getPersonaRepository)
):
    return HospitalizacionesService(hospitalizacionesRepository, atencionUrgenciasRepository, repoDiagnostico, repoDoctor, repoAtencionHospitalizaciones,repoPersona)

def getUrgenciasService(
    triagesRepository: TriagesRepository = Depends(getTriagesRepository),
    atencionUrgenciasRepository: AtencionUrgenciasRepository = Depends(getAtencionUrgenciasRepository),
    repoDoctor: DoctorRepository = Depends(getDoctorRepository),
    repoDiagnostico: DiagnosticoRepository = Depends(getDiagnosticosRepository)
):
    return UrgenciasService(
        triagesRepository,
        atencionUrgenciasRepository,
        repoDoctor,
        repoDiagnostico
    )