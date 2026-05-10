#Repositories
from fastapi import Depends

from db.session import get_db
from services.HospitalizacionesService import HospitalizacionesService
from services.repositories.HospitalizacionesRepository import HospitalizacionesRepository
from services.repositories.AtencionUrgenciasRepository import AtencionUrgenciasRepository

#Repositories
def getAtencionUrgenciasRepository(db = Depends(get_db))-> AtencionUrgenciasRepository:
    return AtencionUrgenciasRepository(db)
def getHospitalizacionesRepository(db = Depends(get_db))-> HospitalizacionesRepository:
    return HospitalizacionesRepository(db)

#Services
def getHospitalizacionesService(
    hospitalizacionesRepository: HospitalizacionesRepository = Depends(getHospitalizacionesRepository),
    atencionUrgenciasRepository: AtencionUrgenciasRepository = Depends(getAtencionUrgenciasRepository)
):
    return HospitalizacionesService(hospitalizacionesRepository, atencionUrgenciasRepository)