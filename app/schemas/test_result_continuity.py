from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TestResultContinuityBase(BaseModel):
    test_run_id: int
    test_point: int
    result_value: Optional[float]
    unit: Optional[str]
    is_na: Optional[bool] = False
    is_passed: Optional[bool]
    observations: Optional[str]
    image_path: Optional[str]

class TestResultContinuityCreate(TestResultContinuityBase):
    pass

class TestResultContinuityUpdate(TestResultContinuityBase):
    pass

class TestResultContinuityOut(TestResultContinuityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
