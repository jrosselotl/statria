from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)

    location_1 = Column(String(100), nullable=True)
    number_location_1 = Column(Integer, nullable=True)

    location_2 = Column(String(100), nullable=True)
    number_location_2 = Column(Integer, nullable=True)

    equipment_type = Column(String(50), nullable=False)
    number_equipment_type = Column(Integer, nullable=True)

    sub_equipment = Column(String(50), nullable=True)
    number_sub_equipment = Column(Integer, nullable=True)

    terminal = Column(String(50), nullable=True)
    power_type = Column(String(50), nullable=True)
    cable_set = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    project = relationship("Project", back_populates="equipment")
    test_run = relationship("TestRun", back_populates="equipment", cascade="all, delete-orphan")
