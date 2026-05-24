from sqlalchemy import Column, BigInteger, String
from db.session import BaseAdmin


class Persona(BaseAdmin):
    __tablename__ = "persona"

    num_documento = Column(BigInteger, primary_key=True)
    nombres       = Column(String(50), nullable=False)
    apellidos     = Column(String(50), nullable=False)


    def __repr__(self):
        return f"<Persona(num_documento={self.num_documento}, nombres={self.nombres}, apellidos={self.apellidos})>"