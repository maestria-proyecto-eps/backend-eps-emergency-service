import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

# ── App y BD ────────────────────────────────────────────────────────────────
from main import app
from db.session import (
    Base, BaseAdmin,
    get_db, get_db_admin,
    get_db_audit, get_db_admin_audit,
)

# ── Auth — se overridea get_current_user_id para cortar HTTPBearer ──────────
# Los routers importan RequireRole de core.dependencias, que llama a
# get_usuario_actual, que llama a get_current_user_id (core.auth_utils),
# que llama a HTTPBearer.  Sin Authorization header → 401 inmediato.
# Overridear get_current_user_id es la única forma de cortarlo en la raíz.
from core.auth_utils import get_current_user_id
from core.dependencias import get_usuario_actual

# ── Modelos ──────────────────────────────────────────────────────────────────
from models.user import USUARIOS, ROLES          # noqa: F401  (registra en BaseAdmin)
from models.AtencionUrgencias import AtencionUrgencias
from models.Hospitalizaciones import Hospitalizaciones
from models.Doctor import Doctor
from models.CatalogoDiagnosticos import CatalogoDiagnosticos
from models.AtencionHospitalizaciones import AtencionHospitalizaciones
from models.Triages import Triages
from models.Persona import Persona              # noqa: F401  (registra en Base)

# ── Engines SQLite en memoria ────────────────────────────────────────────────

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine_admin = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocalAdmin = sessionmaker(autocommit=False, autoflush=False, bind=engine_admin)


# ── Overrides de BD ──────────────────────────────────────────────────────────

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def override_get_db_admin():
    db = TestingSessionLocalAdmin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def override_get_db_audit():
    """
    get_db_audit ejecuta SET LOCAL my.app_user_id en Postgres → falla en CI.
    Se reemplaza por una sesión SQLite sin auditoría.
    """
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def override_get_db_admin_audit():
    """Ídem para get_db_admin_audit."""
    db = TestingSessionLocalAdmin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ── Mock de usuario ──────────────────────────────────────────────────────────

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


# ── Setup global de BD y overrides (scope=session) ──────────────────────────

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Crear tablas en SQLite
    Base.metadata.create_all(bind=engine)
    BaseAdmin.metadata.create_all(bind=engine_admin)

    # ── Overrides de sesión BD ──────────────────────────────────────────────
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_admin] = override_get_db_admin
    app.dependency_overrides[get_db_audit] = override_get_db_audit
    app.dependency_overrides[get_db_admin_audit] = override_get_db_admin_audit

    # ── Override de autenticación ───────────────────────────────────────────
    # 1) Cortamos HTTPBearer en la raíz: get_current_user_id devuelve 1
    #    sin validar ningún token.
    app.dependency_overrides[get_current_user_id] = lambda: 1

    # 2) get_usuario_actual devuelve un usuario mock con rol "Administrador",
    #    lo que hace que RequireRole acepte cualquier endpoint (la condición
    #    en core/dependencias.py es `rol != "Administrador"` para denegar).
    app.dependency_overrides[get_usuario_actual] = lambda: make_mock_usuario("Administrador")

    yield

    # Teardown
    Base.metadata.drop_all(bind=engine)
    BaseAdmin.metadata.drop_all(bind=engine_admin)
    app.dependency_overrides.clear()


# ── Fixture de cliente ───────────────────────────────────────────────────────

@pytest.fixture()
def client():
    return TestClient(app)


# ── Fixtures de sesión directa ───────────────────────────────────────────────

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


# ── Fixtures de datos ────────────────────────────────────────────────────────

@pytest.fixture()
def borrar_hospitalizaciones():
    db = TestingSessionLocal()
    db.query(AtencionHospitalizaciones).delete()
    db.query(Hospitalizaciones).delete()
    db.commit()
    db.close()


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