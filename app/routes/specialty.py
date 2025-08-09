from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.specialty import Specialty
from app.models.test_type import TestType
from app.models.test_project import TestProject
from app.schemas.specialty import SpecialtyCreate, SpecialtyUpdate, SpecialtyOut

router = APIRouter(prefix="/specialty", tags=["Specialty"])

# --- Listar todas
@router.get("/list", response_model=List[SpecialtyOut])
def list_specialties(db: Session = Depends(get_db)):
    return db.query(Specialty).order_by(Specialty.id).all()

# --- Crear
@router.post("/", response_model=SpecialtyOut)
def create_specialty(payload: SpecialtyCreate, db: Session = Depends(get_db)):
    if db.query(Specialty).filter(Specialty.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Specialty already exists")
    obj = Specialty(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# --- Actualizar
@router.put("/{specialty_id}", response_model=SpecialtyOut)
def update_specialty(specialty_id: int, payload: SpecialtyUpdate, db: Session = Depends(get_db)):
    obj = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Specialty not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

# --- Eliminar
@router.delete("/{specialty_id}")
def delete_specialty(specialty_id: int, db: Session = Depends(get_db)):
    obj = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Specialty not found")
    db.delete(obj)
    db.commit()
    return {"message": "Specialty deleted successfully"}

# --- NUEVO: Especialidades con tests habilitados para un proyecto
@router.get("/by_project/{project_id}", response_model=List[SpecialtyOut])
def specialties_by_project(project_id: int, db: Session = Depends(get_db)):
    """
    Devuelve sólo las especialidades que tengan al menos un test_type
    habilitado (is_enabled=True, active=True) en ese proyecto.
    """
    enabled_tt_subq = (
        db.query(TestType.specialty_id)
        .join(TestProject, TestProject.test_type_id == TestType.id)
        .filter(
            TestProject.project_id == project_id,
            TestProject.is_enabled.is_(True),
            TestProject.active.is_(True),
        )
        .distinct()
        .subquery()
    )

    specialties = (
        db.query(Specialty)
        .filter(Specialty.id.in_(select(enabled_tt_subq.c.specialty_id)))
        .order_by(Specialty.id)
        .all()
    )
    return specialties
