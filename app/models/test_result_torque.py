from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class TestResultTorque(Base):
    __tablename__ = "test_result_torque"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_run.id", ondelete="CASCADE"), nullable=False)
    cable_set = Column(Integer, nullable=False)
    test_point = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    observations = Column(Text, nullable=True)
    image_path = Column(String, nullable=True)

    nominal_value = Column(Float, nullable=True)
    verification_value = Column(Float, nullable=True)

    test_run = relationship("TestRun", back_populates="test_result_torque")
