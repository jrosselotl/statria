from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Specialty(Base):
    __tablename__ = "specialty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    test_type = relationship(
        "TestType",
        back_populates="specialty",
        cascade="all, delete-orphan",
        lazy="selectin",
    )