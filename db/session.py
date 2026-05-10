from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

USER = settings.DB_OP_USER
PASSWORD = settings.DB_OP_PASSWORD
HOST = settings.DB_OP_HOST
PORT = settings.DB_OP_PORT
DBNAME = settings.DB_OP_NAME

USER_ADM = settings.DB_ADMIN_USER
PASSWORD_ADM = settings.DB_ADMIN_PASSWORD
HOST_ADM = settings.DB_ADMIN_HOST
PORT_ADM = settings.DB_ADMIN_PORT
DBNAME_ADM = settings.DB_ADMIN_NAME

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
DATABASE_URL_ADM = f"postgresql+psycopg2://{USER_ADM}:{PASSWORD_ADM}@{HOST_ADM}:{PORT_ADM}/{DBNAME_ADM}?sslmode=require"

# Crear engine (sincrónico)
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool
)
engineDMA = create_engine(
    DATABASE_URL_ADM,
    poolclass=NullPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

SessionLocalAdmin = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engineDMA,
)

Base = declarative_base()
BaseAdmin = declarative_base()


# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_admin():
    db = SessionLocalAdmin()
    try:
        yield db
    finally:
        db.close()
