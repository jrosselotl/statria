from pydantic import BaseModel
from typing import Optional

class TestTypeBase(BaseModel):
    name: str
    specialty_id: int
    description: Optional[str] = None

class TestTypeCreate(TestTypeBase):
    pass

class TestTypeUpdate(TestTypeBase):
    pass

class TestTypeOut(TestTypeBase):
    id: int

    class Config:
        orm_mode = True
