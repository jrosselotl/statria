from pydantic import BaseModel
from typing import Optional

class TestProjectBase(BaseModel):
    project_id: int
    test_type_id: int
    active: Optional[bool] = True

class TestProjectCreate(TestProjectBase):
    pass

class TestProjectOut(TestProjectBase):
    id: int

    class Config:
        orm_mode = True
