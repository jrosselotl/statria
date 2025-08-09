from pydantic import BaseModel
from typing import Optional

class TestResultBase(BaseModel):
    test_run_id: int
    cable_set: Optional[str]
    point_from: Optional[str]
    point_to: Optional[str]
    result_value: Optional[float]
    is_na: Optional[bool] = False
    approved: Optional[bool]
    observation: Optional[str]
    photo_url: Optional[str]

class TestResultCreate(TestResultBase):
    pass

class TestResultUpdate(TestResultBase):
    pass

class TestResultOut(TestResultBase):
    id: int

    class Config:
        orm_mode = True
