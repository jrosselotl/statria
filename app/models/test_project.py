# app/models/test_project.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class TestProject(Base):
    __tablename__ = "test_project"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    test_type_id = Column(Integer, ForeignKey("test_type.id"), nullable=False)

    # IMPORTANTES: existen en la DB
    is_enabled = Column(Boolean, default=True, nullable=True)
    active = Column(Boolean, default=True, nullable=True)

    # Relaciones (opcionales pero útiles)
    project = relationship("Project", back_populates="test_project", lazy="joined")
    test_type = relationship("TestType", back_populates="test_project", lazy="joined")

    __table_args__ = (
        UniqueConstraint("project_id", "test_type_id", name="test_project_project_id_test_type_id_key"),
    )
