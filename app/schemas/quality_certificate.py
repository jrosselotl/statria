from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QualityCertificateBase(BaseModel):
    name: str
    pdf_url: str
    uploaded_by: Optional[int] = None

class QualityCertificateCreate(QualityCertificateBase):
    pass

class QualityCertificateOut(QualityCertificateBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True