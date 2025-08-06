from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.test_type import TestType
from app.schemas.test_type import TestTypeCreate, TestTypeUpdate, TestTypeOut

router = APIRouter(prefix="/test_type", tags=["Test Type"])

# 🔹 Listar todos los tipos de test
@router.get("/list", response_model=List[TestTypeOut])
def list_test_types(db: Session = Depends(get_db)):
    return db.query(TestType).all()

# 🔹 Crear nuevo tipo de test
@router.post("/", response_model=TestTypeOut)
def create_test_type(test_type: TestTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(TestType).filter(TestType.name == test_type.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Test type already exists")
    new_type = TestType(**test_type.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

# 🔹 Actualizar tipo de test
@router.put("/{test_type_id}", response_model=TestTypeOut)
def update_test_type(test_type_id: int, test_type: TestTypeUpdate, db: Session = Depends(get_db)):
    db_type = db.query(TestType).filter(TestType.id == test_type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Test type not found")
    for key, value in test_type.dict().items():
        setattr(db_type, key, value)
    db.commit()
    db.refresh(db_type)
    return db_type

# 🔹 Eliminar tipo de test
@router.delete("/{test_type_id}")
def delete_test_type(test_type_id: int, db: Session = Depends(get_db)):
    db_type = db.query(TestType).filter(TestType.id == test_type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Test type not found")
    db.delete(db_type)
    db.commit()
    return {"message": "Test type deleted successfully"}
