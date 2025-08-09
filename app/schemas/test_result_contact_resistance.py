from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_result_contact_resistance import TestResultContactResistance
from app.schemas.test_result_contact_resistance import (
    TestResultContactResistanceCreate,
    TestResultContactResistanceOut
)

router = APIRouter(prefix="/contact_resistance", tags=["Contact Resistance"])

@router.post("/create", response_model=TestResultContactResistanceOut)
def create_result(data: TestResultContactResistanceCreate, db: Session = Depends(get_db)):
    result = TestResultContactResistance(**data.dict())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

@router.get("/list/{test_run_id}", response_model=list[TestResultContactResistanceOut])
def list_results(test_run_id: int, db: Session = Depends(get_db)):
    return db.query(TestResultContactResistance).filter_by(test_run_id=test_run_id).all()

@router.delete("/delete/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(TestResultContactResistance).get(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"message": "Deleted successfully"}
