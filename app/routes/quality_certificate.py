from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.quality_certificate import QualityCertificate
from app.schemas.quality_certificate import QualityCertificateCreate, QualityCertificateOut

router = APIRouter(prefix="/quality_certificate", tags=["Quality quality_certificate"])

@router.get("/list", response_model=List[QualityCertificateOut])
def list_certificates(db: Session = Depends(get_db)):
    return db.query(QualityCertificate).all()

@router.post("/", response_model=QualityCertificateOut)
def create_certificate(data: QualityCertificateCreate, db: Session = Depends(get_db)):
    quality_certificate = QualityCertificate(**data.dict())
    db.add(quality_certificate)
    db.commit()
    db.refresh(quality_certificate)
    return quality_certificate

@router.delete("/{certificate_id}")
def delete_certificate(certificate_id: int, db: Session = Depends(get_db)):
    quality_certificate = db.query(QualityCertificate).filter_by(id=certificate_id).first()
    if not quality_certificate:
        raise HTTPException(status_code=404, detail="quality_certificate not found")
    
    db.delete(quality_certificate)
    db.commit()
    return {"message": "quality_certificate deleted successfully"}
