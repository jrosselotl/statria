from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EquipmentBase(BaseModel):
    project_id: Optional[int]
    code: str
    description: Optional[str]

    location_1: Optional[str]
    number_location_1: Optional[int]

    location_2: Optional[str]
    number_location_2: Optional[int]

    equipment_type: str
    number_equipment_type: Optional[int]

    sub_equipment: Optional[str]
    number_sub_equipment: Optional[int]

    terminal: Optional[str]
    power_type: Optional[str]
    cable_set: Optional[int]

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentOut(EquipmentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
