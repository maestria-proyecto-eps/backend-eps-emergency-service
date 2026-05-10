#Repositories
from fastapi import Depends

from db.session import get_db, get_db_admin
from services.HospitalizacionesService import HospitalizacionesService
from services.repositories.AtencionHospitalizacionesRepository import AtencionHospitalizacionesRepository
from services.repositories.DiagnosticoRepository import DiagnosticoRepository
from services.repositories.DoctorRepository import DoctorRepository
from services.repositories.HospitalizacionesRepository import HospitalizacionesRepository
from services.repositories.AtencionUrgenciasRepository import AtencionUrgenciasRepository

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
#Services
def getHospitalizacionesService(
    hospitalizacionesRepository: HospitalizacionesRepository = Depends(getHospitalizacionesRepository),
    atencionUrgenciasRepository: AtencionUrgenciasRepository = Depends(getAtencionUrgenciasRepository),
    repoAtencionHospitalizaciones: AtencionHospitalizacionesRepository = Depends(getAtencionHospitalizacionesRepository),
    repoDiagnostico: DiagnosticoRepository = Depends(getDiagnosticosRepository),
    repoDoctor: DoctorRepository = Depends(getDoctorRepository)
):
    return HospitalizacionesService(hospitalizacionesRepository, atencionUrgenciasRepository, repoDiagnostico, repoDoctor, repoAtencionHospitalizaciones)