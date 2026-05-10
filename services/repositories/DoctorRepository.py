from models.Doctor import Doctor


class DoctorRepository:
    def __init__(self, session):
        self.session = session

    def existe_doctor(self, id_doctor: int) -> bool:
        return self.session.query(Doctor).filter_by(id_medico=id_doctor).first() is not None