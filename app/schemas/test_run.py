from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TestRunBase(BaseModel):
    equipment_id: int
    user_id: int
    test_type_id: int
    certificate_id: Optional[int] = None
    project_id: int
    general_image: Optional[str] = None
    general_images: Optional[str] = None


class TestRunCreate(TestRunBase):
    pass


class TestRunOut(TestRunBase):
    id: int
    started_at: datetime

    class Config:
        orm_mode = True
