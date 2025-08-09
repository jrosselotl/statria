from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class TestResultContactResistance(Base):
    __tablename__ = "test_result_contact_resistance"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_run.id", ondelete="CASCADE"))
    cable_set = Column(Integer, nullable=True)
    test_point = Column(String, nullable=True)
    result_value = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    observations = Column(String, nullable=True)
    image_path = Column(String, nullable=True)

    test_run = relationship("TestRun", back_populates="test_result_contact_resistance")