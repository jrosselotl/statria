from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.test_result_continuity import TestResultContinuity
from app.schemas.test_result_continuity import (
    TestResultContinuityCreate,
    TestResultContinuityUpdate,
    TestResultContinuityOut
)

router = APIRouter(prefix="/test_result_continuity", tags=["Test Result - Continuity"])

# 🔹 Listar
@router.get("/list", response_model=List[TestResultContinuityOut])
def list_results(db: Session = Depends(get_db)):
    return db.query(TestResultContinuity).all()

# 🔹 Crear
@router.post("/", response_model=TestResultContinuityOut)
def create_result(data: TestResultContinuityCreate, db: Session = Depends(get_db)):
    new_result = TestResultContinuity(**data.dict())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

# 🔹 Actualizar
@router.put("/{result_id}", response_model=TestResultContinuityOut)
def update_result(result_id: int, data: TestResultContinuityUpdate, db: Session = Depends(get_db)):
    result = db.query(TestResultContinuity).filter_by(id=result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    for key, value in data.dict().items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result

# 🔹 Eliminar
@router.delete("/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(TestResultContinuity).filter_by(id=result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"message": "Continuity test result deleted successfully"}
