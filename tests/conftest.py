import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from db.session import Base, BaseAdmin, get_db, get_db_admin
from main import app
from models.AtencionUrgencias import AtencionUrgencias
from models.Hospitalizaciones import Hospitalizaciones

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuración DB2 (admin)
SQLALCHEMY_DATABASE_URL_ADMIN = "sqlite://"
engine_admin = create_engine(
    SQLALCHEMY_DATABASE_URL_ADMIN,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocalAdmin = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_admin,
)

def override_get_db_admin():
    db = TestingSessionLocalAdmin()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    BaseAdmin.metadata.create_all(bind=engine_admin)
    app.dependency_overrides[get_db_admin] = override_get_db_admin

    yield
    Base.metadata.drop_all(bind=engine)
    BaseAdmin.metadata.drop_all(bind=engine_admin)

    app.dependency_overrides.clear()

@pytest.fixture
def crear_urgencia():
    db = TestingSessionLocal()
    urgencia = AtencionUrgencias(
        id_urgencia=50,
        id_doctor=12345,
        observaciones="Paciente con dolor abdominal",
        tratamiento="Administrar analgésicos",
        id_triage=1,
        id_diagnostico=1
    )
    db.add(urgencia)
    db.commit()
    db.refresh(urgencia)
    yield urgencia

@pytest.fixture
def crear_hospitalizacion():
    db = TestingSessionLocal()
    hospitalizacion = Hospitalizaciones(
        num_cama=101,
        ingreso=datetime.datetime(2024, 6, 1, 10, 0),
        salida=None,
        estado=0,
        id_urgencia=50
    )
    db.add(hospitalizacion)
    db.commit()
    db.refresh(hospitalizacion)
    yield hospitalizacion
    
@pytest.fixture()
def borrar_hospitalizaciones():
    db = TestingSessionLocal()
    db.query(Hospitalizaciones).delete()
    db.commit()
    
@pytest.fixture()
def client():
    return TestClient(app)