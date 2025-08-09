from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from app.models.quality_certificate import QualityCertificate
from app.models.test_result_mapping import TestResultMapping

class TestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    test_type_id = Column(Integer, ForeignKey("test_type.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    quality_certificate_id = Column(Integer, ForeignKey("quality_certificate.id"))

    general_images = Column(ARRAY(Text), nullable=True)

    # Relaciones
    equipment = relationship("Equipment", back_populates="test_run")
    user = relationship("User", back_populates="test_run")
    test_type = relationship("TestType", back_populates="test_run")
    quality_certificate = relationship("QualityCertificate", back_populates="test_run")
    project = relationship("Project", back_populates="test_run")
    test_result_mapping = relationship("TestResultMapping", back_populates="test_run", cascade="all, delete-orphan")

    test_result_continuity = relationship(
        "TestResultContinuity", back_populates="test_run", cascade="all, delete-orphan"
    )
    test_result_insulation = relationship(
        "TestResultInsulation", back_populates="test_run", cascade="all, delete-orphan"
    )
    test_result_contact_resistance = relationship(
        "TestResultContactResistance", back_populates="test_run", cascade="all, delete-orphan"
    )
    test_result_torque = relationship(
        "TestResultTorque", back_populates="test_run", cascade="all, delete-orphan"
    )
