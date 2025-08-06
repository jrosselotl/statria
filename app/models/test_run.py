from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    test_type_id = Column(Integer, ForeignKey("test_type.id", ondelete="CASCADE"), nullable=False)
    certificate_id = Column(Integer, ForeignKey("certificate.id"), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)

    general_image = Column(Text, nullable=True)
    general_images = Column(Text, nullable=True)

    # Relaciones
    equipment = relationship("Equipment", back_populates="test_run")
    user = relationship("User", back_populates="test_run")
    test_type = relationship("TestType", back_populates="test_run")
    certificate = relationship("Certificate", back_populates="test_run")
    project = relationship("Project", back_populates="test_run")

    result_continuity = relationship("ResultContinuity", back_populates="test_run", cascade="all, delete-orphan")
    result_insulation = relationship("ResultInsulation", back_populates="test_run", cascade="all, delete-orphan")
    result_contact_resistance = relationship("ResultContactResistance", back_populates="test_run", cascade="all, delete-orphan")
    result_torque = relationship("ResultTorque", back_populates="test_run", cascade="all, delete-orphan")
