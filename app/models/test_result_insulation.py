from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TestResultInsulation(Base):
    __tablename__ = "test_result_insulation"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_run.id", ondelete="CASCADE"))
    cable_set = Column(Integer, nullable=True)
    test_point = Column(String, nullable=False)
    result_value = Column(Float, nullable=True)
    time_applied = Column(Integer, nullable=True)
    unit = Column(String, nullable=True)
    observations = Column(String, nullable=True)
    image_path = Column(String, nullable=True)

    test_run = relationship("TestRun", back_populates="test_result_insulation")