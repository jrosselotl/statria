from pydantic import BaseModel, Field
from typing import Optional

class TestResultInsulationBase(BaseModel):
    cable_set: Optional[int] = None
    test_point: str
    result_value: Optional[float] = None
    time_applied: Optional[int] = None
    unit: Optional[str] = None
    observations: Optional[str] = None
    image_path: Optional[str] = None

class TestResultInsulationCreate(TestResultInsulationBase):
    test_run_id: int

class TestResultInsulationOut(TestResultInsulationBase):
    id: int
    test_run_id: int

    class Config:
        from_attributes = True