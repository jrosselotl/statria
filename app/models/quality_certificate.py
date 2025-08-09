from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class QualityCertificate(Base):
    __tablename__ = "quality_certificate"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    pdf_url = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, nullable=True)

    assignments = relationship("CertificateAssignment", back_populates="quality_certificate")
    test_run = relationship("TestRun", back_populates="quality_certificate")
