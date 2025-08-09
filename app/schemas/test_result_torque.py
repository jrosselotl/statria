from pydantic import BaseModel
from typing import Optional

class TestResultTorqueBase(BaseModel):
    test_point: str
    cable_set: int
    unit: Optional[str] = None
    observations: Optional[str] = None
    image_path: Optional[str] = None
    nominal_value: Optional[float] = None
    verification_value: Optional[float] = None

class TestResultTorqueCreate(TestResultTorqueBase):
    test_run_id: int

class TestResultTorqueOut(TestResultTorqueBase):
    id: int
    test_run_id: int

    class Config:
        from_attributes = True
