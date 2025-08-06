from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.test_result import TestResult
from app.schemas.test_result import TestResultCreate, TestResultUpdate, TestResultOut

router = APIRouter(prefix="/test_result", tags=["Test Result"])

# 🔹 Listar todos
@router.get("/list", response_model=List[TestResultOut])
def list_test_results(db: Session = Depends(get_db)):
    return db.query(TestResult).all()

# 🔹 Crear uno
@router.post("/", response_model=TestResultOut)
def create_test_result(result: TestResultCreate, db: Session = Depends(get_db)):
    new_result = TestResult(**result.dict())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

# 🔹 Actualizar uno
@router.put("/{result_id}", response_model=TestResultOut)
def update_test_result(result_id: int, result: TestResultUpdate, db: Session = Depends(get_db)):
    db_result = db.query(TestResult).filter(TestResult.id == result_id).first()
    if not db_result:
        raise HTTPException(status_code=404, detail="Test result not found")

    for key, value in result.dict().items():
        setattr(db_result, key, value)
    db.commit()
    db.refresh(db_result)
    return db_result

# 🔹 Eliminar uno
@router.delete("/{result_id}")
def delete_test_result(result_id: int, db: Session = Depends(get_db)):
    db_result = db.query(TestResult).filter(TestResult.id == result_id).first()
    if not db_result:
        raise HTTPException(status_code=404, detail="Test result not found")

    db.delete(db_result)
    db.commit()
    return {"message": "Test result deleted successfully"}
