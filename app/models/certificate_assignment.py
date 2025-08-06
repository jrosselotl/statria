from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CertificateAssignment(Base):
    __tablename__ = "certificate_assignment"

    id = Column(Integer, primary_key=True, index=True)
    quality_certificate_id = Column(Integer, ForeignKey("quality_certificate.id"), nullable=False)
    test_type_id = Column(Integer, ForeignKey("test_type.id"), nullable=False)

    # Relaciones
    quality_certificate = relationship("QualityCertificate", back_populates="assignments")
    test_type = relationship("TestType", back_populates="assignments")
