from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.specialty import Specialty
from app.schemas.specialty import SpecialtyCreate, SpecialtyUpdate, SpecialtyOut

router = APIRouter(prefix="/specialty", tags=["Specialty"])

# 🔹 Listar todas las especialidades
@router.get("/list", response_model=List[SpecialtyOut])
def list_specialties(db: Session = Depends(get_db)):
    return db.query(Specialty).all()

# 🔹 Crear especialidad
@router.post("/", response_model=SpecialtyOut)
def create_specialty(specialty: SpecialtyCreate, db: Session = Depends(get_db)):
    existing = db.query(Specialty).filter(Specialty.name == specialty.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Specialty already exists")
    new_specialty = Specialty(**specialty.dict())
    db.add(new_specialty)
    db.commit()
    db.refresh(new_specialty)
    return new_specialty

# 🔹 Actualizar especialidad
@router.put("/{specialty_id}", response_model=SpecialtyOut)
def update_specialty(specialty_id: int, specialty: SpecialtyUpdate, db: Session = Depends(get_db)):
    db_specialty = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    for key, value in specialty.dict().items():
        setattr(db_specialty, key, value)
    db.commit()
    db.refresh(db_specialty)
    return db_specialty

# 🔹 Eliminar especialidad
@router.delete("/{specialty_id}")
def delete_specialty(specialty_id: int, db: Session = Depends(get_db)):
    db_specialty = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    db.delete(db_specialty)
    db.commit()
    return {"message": "Specialty deleted successfully"}
