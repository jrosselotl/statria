from pydantic import BaseModel
from typing import Optional

class TestResultContactResistanceBase(BaseModel):
    cable_set: Optional[int]
    test_point: Optional[str]
    result_value: Optional[float]
    unit: Optional[str]
    observations: Optional[str]
    image_path: Optional[str]

class TestResultContactResistanceCreate(TestResultContactResistanceBase):
    test_run_id: int

class TestResultContactResistanceOut(TestResultContactResistanceBase):
    id: int
    test_run_id: int

    class Config:
        from_attributes = True
