import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from db.session import Base, BaseAdmin, get_db, get_db_admin
from main import app
from models.AtencionUrgencias import AtencionUrgencias
from models.Hospitalizaciones import Hospitalizaciones
from models.Doctor import Doctor
from models.CatalogoDiagnosticos import CatalogoDiagnosticos
from models.AtencionHospitalizaciones import AtencionHospitalizaciones
from models.Triages import Triages
from models.Persona import Persona

# USUARIOS y ROLES usan BaseAdmin — importar para que BaseAdmin.metadata
# los registre antes de create_all y el FK usuarios->persona se resuelva.
from models.user import USUARIOS, ROLES  # noqa: F401

from core.dependencias import get_usuario_actual
from core.auth_utils import get_current_user_id  # ← NUEVO: cortar la cadena HTTPBearer

# ---------------------------------------------------------------------------
# Engines SQLite en memoria
# ---------------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLALCHEMY_DATABASE_URL_ADMIN = "sqlite://"
engine_admin = create_engine(
    SQLALCHEMY_DATABASE_URL_ADMIN,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocalAdmin = sessionmaker(autocommit=False, autoflush=False, bind=engine_admin)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_db_admin():
    db = TestingSessionLocalAdmin()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Helpers para mocks de usuario
# ---------------------------------------------------------------------------

def make_mock_usuario(rol_nombre: str) -> USUARIOS:
    """Construye un USUARIOS en memoria con su rol ya cargado."""
    rol = ROLES(id_rol=1, nombre_rol=rol_nombre)
    user = USUARIOS(
        id_usuario=1,
        num_documento=999999999,
        password="x",
        id_rol=1,
        estado=True,
        intentos_login=0,
    )
    user.rol = rol
    return user


# ---------------------------------------------------------------------------
# Fixtures de sesión
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    BaseAdmin.metadata.create_all(bind=engine_admin)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_admin] = override_get_db_admin

    # ── CORRECCIÓN CLAVE ────────────────────────────────────────────────────
    # HTTPBearer lanza 401 cuando no hay header Authorization, incluso antes
    # de que el override de get_usuario_actual tenga efecto, porque FastAPI
    # resuelve el árbol de dependencias completo:
    #   RequireRole → get_usuario_actual → get_current_user_id → HTTPBearer → 401
    #
    # Solución: cortar la cadena en la raíz sobreescribiendo get_current_user_id
    # para que devuelva un user_id ficticio sin tocar el token.
    app.dependency_overrides[get_current_user_id] = lambda: 1  # ← NUEVO

    # get_usuario_actual también se overridea para evitar la consulta a BD
    # y devolver directamente el usuario mock con rol "Administrador"
    # (pasa cualquier RequireRole gracias a la lógica `!= "Administrador"` del guard).
    app.dependency_overrides[get_usuario_actual] = lambda: make_mock_usuario("Administrador")

    yield

    Base.metadata.drop_all(bind=engine)
    BaseAdmin.metadata.drop_all(bind=engine_admin)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Fixtures de datos
# ---------------------------------------------------------------------------

@pytest.fixture
def crear_urgencia():
    db = TestingSessionLocal()
    urgencia = db.query(AtencionUrgencias).filter(AtencionUrgencias.id_urgencia == 50).first()
    if not urgencia:
        urgencia = AtencionUrgencias(
            id_urgencia=50,
            id_doctor=12345,
            observaciones="Paciente con dolor abdominal",
            tratamiento="Administrar analgésicos",
            id_triage=1,
            id_diagnostico=1,
        )
        db.add(urgencia)
        db.commit()
        db.refresh(urgencia)
    yield urgencia
    db.close()


@pytest.fixture
def crear_hospitalizacion():
    db = TestingSessionLocal()
    hospitalizacion = db.query(Hospitalizaciones).filter(Hospitalizaciones.id_urgencia == 50).first()
    if not hospitalizacion:
        hospitalizacion = Hospitalizaciones(
            num_cama=101,
            ingreso=datetime.datetime(2024, 6, 1, 10, 0),
            salida=None,
            estado=0,
            id_urgencia=50,
        )
        db.add(hospitalizacion)
        db.commit()
        db.refresh(hospitalizacion)
    yield hospitalizacion
    db.close()


@pytest.fixture()
def borrar_hospitalizaciones():
    db = TestingSessionLocal()
    db.query(Hospitalizaciones).delete()
    db.commit()


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def db_admin_session():
    db = TestingSessionLocalAdmin()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture
def crear_doctor():
    db = TestingSessionLocalAdmin()
    doctor = db.query(Doctor).filter(Doctor.id_medico == 12345).first()
    if not doctor:
        doctor = Doctor(
            id_medico=12345,
            num_licencia=123456,
            id_especialidad=1,
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
    yield doctor
    db.close()


@pytest.fixture
def crear_diagnostico():
    db = TestingSessionLocal()
    diagnostico = db.query(CatalogoDiagnosticos).filter(CatalogoDiagnosticos.id_diagnostico == 1).first()
    if not diagnostico:
        diagnostico = CatalogoDiagnosticos(
            id_diagnostico=1,
            nombre_enfermedad="Gripe",
        )
        db.add(diagnostico)
        db.commit()
        db.refresh(diagnostico)
    yield diagnostico
    db.close()


@pytest.fixture
def crear_atencion_hospitalizacion(crear_hospitalizacion, crear_doctor, crear_diagnostico):
    db = TestingSessionLocal()
    atencion = db.query(AtencionHospitalizaciones).filter(
        AtencionHospitalizaciones.id_hospitalizacion == crear_hospitalizacion.id_hospitalizacion,
        AtencionHospitalizaciones.id_doctor == 12345,
    ).first()
    if not atencion:
        atencion = AtencionHospitalizaciones(
            id_doctor=12345,
            fecha_atencionh=datetime.datetime.now(),
            id_diagnostico=1,
            id_hospitalizacion=crear_hospitalizacion.id_hospitalizacion,
            observaciones="Observaciones de prueba",
            tratamiento="Tratamiento de prueba",
        )
        db.add(atencion)
        db.commit()
        db.refresh(atencion)
    yield atencion
    db.close()