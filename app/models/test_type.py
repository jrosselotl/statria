from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TestType(Base):
    __tablename__ = "test_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    specialty_id = Column(Integer, ForeignKey("specialty.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=True)


    specialty = relationship("Specialty", back_populates="test_type")
    test_project = relationship("TestProject", back_populates="test_type", cascade="all, delete-orphan")
    test_run = relationship("TestRun", back_populates="test_type")
    assignments = relationship("CertificateAssignment", back_populates="test_type")
