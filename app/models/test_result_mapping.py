from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TestResultMapping(Base):
    __tablename__ = "test_result_mapping"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_run.id"), nullable=False)

    cable_set = Column(String(50), nullable=True)
    point_from = Column(String(50), nullable=True)
    point_to = Column(String(50), nullable=True)

    result_value = Column(Numeric, nullable=True)
    is_na = Column(Boolean, default=False)
    approved = Column(Boolean, nullable=True)

    observation = Column(Text, nullable=True)
    photo_url = Column(Text, nullable=True)

    # Relaciones
    test_run = relationship("TestRun", back_populates="test_result_mapping")
