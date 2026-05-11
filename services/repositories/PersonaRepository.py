from db import session
from models.Persona import Persona


class PersonaRepository:
    def __init__(self, db:session):
        self.db = db

    def get_persona_por_id(self, id_persona: int):
        return self.db.query(Persona).filter(Persona.num_documento == id_persona).first()