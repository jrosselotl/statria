from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EquipmentType(Base):
    __tablename__ = "equipment_type"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=True)

    equipment_type = Column(String(100), nullable=False)
    number_equipment_type = Column(Integer, nullable=True)

    sub_equipment = Column(String(100), nullable=True)
    number_sub_equipment = Column(Integer, nullable=True)

    # Relaciones
    project = relationship("Project", back_populates="equipment_type", lazy="joined")
