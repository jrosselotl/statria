from pydantic import BaseModel
from typing import Optional

class EquipmentTypeOut(BaseModel):
    id: int
    project_id: Optional[int]
    equipment_type: str
    number_equipment_type: Optional[int]
    sub_equipment: Optional[str]
    number_sub_equipment: Optional[int]

    class Config:
        orm_mode = True
