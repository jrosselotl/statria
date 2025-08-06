from sqlalchemy import Column, Integer, Numeric, String, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TestResultContinuity(Base):
    __tablename__ = "test_result_continuity"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_run.id"), nullable=False)
    test_point = Column(Integer, nullable=False)
    result_value = Column(Numeric(10, 3), nullable=True)
    unit = Column(String(20), nullable=True)
    is_na = Column(Boolean, default=False)
    is_passed = Column(Boolean, nullable=True)
    observations = Column(Text, nullable=True)
    image_path = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relaciones
    test_run = relationship("TestRun", back_populates="continuity_results")
