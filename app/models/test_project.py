from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class TestProject(Base):
    __tablename__ = "test_project"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    test_type_id = Column(Integer, ForeignKey("test_type.id", ondelete="CASCADE"), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    # índices/únicos
    __table_args__ = (
        UniqueConstraint("project_id", "test_type_id", name="ux_test_project_project_test"),
    )

    # relaciones (opcionales si las usas)
    project = relationship("Project", back_populates="test_project")
    test_type = relationship("TestType", back_populates="test_project")
