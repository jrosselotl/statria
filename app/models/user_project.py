from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User
from app.models.project import Project

class UserProject(Base):
    __tablename__ = "user_project"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    project_id = Column(Integer, ForeignKey("project.id"))

    user = relationship("User", back_populates="project")
    project = relationship("Project")
