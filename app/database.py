from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar .env si quieres usarlo después
load_dotenv()

# ✅ Tu nueva URL de conexión local en el VPS
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el engine
engine = create_engine(
    DATABASE_URL,
    echo=False,                 # logs SQL si True
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={}             # SIN SSL ya que estás en servidor propio
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para inyectar DB en rutas FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
