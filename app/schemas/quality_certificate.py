from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.quality_certificate import QualityCertificate
from app.schemas.quality_certificate import QualityCertificateCreate, QualityCertificateOut

router = APIRouter(prefix="/certificate", tags=["Quality Certificate"])

@router.get("/list", response_model=List[QualityCertificateOut])
def list_certificates(db: Session = Depends(get_db)):
    return db.query(QualityCertificate).all()

@router.post("/", response_model=QualityCertificateOut)
def create_certificate(data: QualityCertificateCreate, db: Session = Depends(get_db)):
    certificate = QualityCertificate(**data.dict())
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate

@router.delete("/{certificate_id}")
def delete_certificate(certificate_id: int, db: Session = Depends(get_db)):
    certificate = db.query(QualityCertificate).filter_by(id=certificate_id).first()
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    db.delete(certificate)
    db.commit()
    return {"message": "Certificate deleted successfully"}
