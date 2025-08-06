from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.certificate_assignment import CertificateAssignment
from app.schemas.certificate_assignment import CertificateAssignmentCreate, CertificateAssignmentOut

router = APIRouter(prefix="/certificate-assignment", tags=["Certificate Assignment"])

@router.get("/list", response_model=List[CertificateAssignmentOut])
def list_assignments(db: Session = Depends(get_db)):
    return db.query(CertificateAssignment).all()

@router.post("/", response_model=CertificateAssignmentOut)
def create_assignment(data: CertificateAssignmentCreate, db: Session = Depends(get_db)):
    assignment = CertificateAssignment(**data.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(CertificateAssignment).filter_by(id=assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}
