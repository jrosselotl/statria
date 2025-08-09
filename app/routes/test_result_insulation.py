from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_result_insulation import TestResultInsulation
from app.schemas.test_result_insulation import (
    TestResultInsulationCreate,
    TestResultInsulationOut
)

router = APIRouter(prefix="/test-result-insulation", tags=["Test Result Insulation"])

@router.post("/", response_model=TestResultInsulationOut)
def create_result(result: TestResultInsulationCreate, db: Session = Depends(get_db)):
    db_result = TestResultInsulation(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@router.get("/{test_run_id}", response_model=list[TestResultInsulationOut])
def get_results(test_run_id: int, db: Session = Depends(get_db)):
    return db.query(TestResultInsulation).filter(TestResultInsulation.test_run_id == test_run_id).all()

@router.delete("/{id}")
def delete_result(id: int, db: Session = Depends(get_db)):
    result = db.query(TestResultInsulation).filter(TestResultInsulation.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"message": "Deleted successfully"}
