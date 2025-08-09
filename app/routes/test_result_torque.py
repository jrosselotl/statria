from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.test_result_torque import TestResultTorque
from app.schemas.test_result_torque import TestResultTorqueCreate, TestResultTorqueOut

router = APIRouter(prefix="/test_result/torque", tags=["TestResult - Torque"])

@router.post("/", response_model=TestResultTorqueOut)
def create_result(result: TestResultTorqueCreate, db: Session = Depends(get_db)):
    db_result = TestResultTorque(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@router.get("/{test_run_id}", response_model=List[TestResultTorqueOut])
def get_results_by_test_run(test_run_id: int, db: Session = Depends(get_db)):
    return db.query(TestResultTorque).filter(TestResultTorque.test_run_id == test_run_id).all()

@router.delete("/{test_run_id}")
def delete_results_by_test_run(test_run_id: int, db: Session = Depends(get_db)):
    deleted = db.query(TestResultTorque).filter(TestResultTorque.test_run_id == test_run_id).delete()
    db.commit()
    return {"deleted": deleted}
