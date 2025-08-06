from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.database import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    location_1 = Column(String(50), nullable=False)
    number_location_1 = Column(JSON, nullable=True)  # Example: [1,2,3]
    location_2 = Column(String(50), nullable=True)
    number_location_2 = Column(JSON, nullable=True)  # Example: [1,2,3]
