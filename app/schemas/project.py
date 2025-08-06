from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ------- Project -------
class ProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    company_id: Optional[int] = None
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    client_logo: Optional[str] = None
    subcontractor_logo: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    company_id: Optional[int] = None
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    client_logo: Optional[str] = None
    subcontractor_logo: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    class Config:
        from_attributes = True  # pydantic v2
        # orm_mode = True        # pydantic v1


# ------- TestProject (relación) -------
class TestProjectBase(BaseModel):
    test_type_id: int
    active: bool = True

class TestProjectOut(TestProjectBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True
