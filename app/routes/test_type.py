from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.test_type import TestType
from app.models.test_project import TestProject
from app.schemas.test_type import TestTypeCreate, TestTypeUpdate, TestTypeOut

router = APIRouter(prefix="/test_type", tags=["Test Type"])

# --- Listar todos (catálogo)
@router.get("/", response_model=List[TestTypeOut])
def list_test_types(db: Session = Depends(get_db)):
    return db.query(TestType).order_by(TestType.id).all()

# --- Crear
@router.post("/", response_model=TestTypeOut)
def create_test_type(payload: TestTypeCreate, db: Session = Depends(get_db)):
    if db.query(TestType).filter(TestType.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Test type already exists")
    obj = TestType(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# --- Actualizar
@router.put("/{test_type_id}", response_model=TestTypeOut)
def update_test_type(test_type_id: int, payload: TestTypeUpdate, db: Session = Depends(get_db)):
    obj = db.query(TestType).filter(TestType.id == test_type_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Test type not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

# --- Eliminar
@router.delete("/{test_type_id}")
def delete_test_type(test_type_id: int, db: Session = Depends(get_db)):
    obj = db.query(TestType).filter(TestType.id == test_type_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Test type not found")
    db.delete(obj)
    db.commit()
    return {"message": "Test type deleted successfully"}

# --- NUEVO: Tests habilitados por proyecto y especialidad
@router.get("/by_project", response_model=List[TestTypeOut])
def list_by_project_and_specialty(
    project_id: int = Query(...),
    specialty_id: int = Query(...),
    db: Session = Depends(get_db),
):
    items = (
        db.query(TestType)
        .join(TestProject, TestProject.test_type_id == TestType.id)
        .filter(
            TestProject.project_id == project_id,
            TestProject.is_enabled.is_(True),
            TestProject.active.is_(True),
            TestType.specialty_id == specialty_id,
        )
        .order_by(TestType.id)
        .all()
    )
    return items
