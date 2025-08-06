from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Specialty(Base):
    __tablename__ = "specialty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    #Relaciones
    test_types = relationship("TestType", back_populates="specialty")