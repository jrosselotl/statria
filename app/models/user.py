from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    technician = "technician"
    project = "project"

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="technician")  # admin, technician, project
    company_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    user_mode = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    user_project = relationship("UserProject", back_populates="user", cascade="all, delete-orphan")
    test_performed = relationship("TestPerformed", back_populates="user", cascade="all, delete-orphan")
