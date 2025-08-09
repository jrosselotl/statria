from pydantic import BaseModel
from typing import List, Optional

class LocationBase(BaseModel):
    location_1: str
    number_location_1: Optional[List[int]] = None
    location_2: Optional[str] = None
    number_location_2: Optional[List[int]] = None

class LocationCreate(LocationBase):
    project_id: int

class LocationResponse(LocationBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True
