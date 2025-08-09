from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    test_project = relationship("TestProject", back_populates="project", cascade="all, delete-orphan")
    location = relationship("Location",back_populates="project")
    equipment_type = relationship("EquipmentType", back_populates="project")
    equipment = relationship("Equipment", back_populates="project")
    test_run = relationship("TestRun", back_populates="project")