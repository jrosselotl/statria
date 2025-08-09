from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipment_type import EquipmentType
from app.schemas.equipment_type import EquipmentTypeOut

router = APIRouter(prefix="/equipment_type", tags=["Equipment Type"])

@router.get("/list")
def list_equipment_type(db: Session = Depends(get_db)):
    equipment_type = db.query(EquipmentType).all()
    return [
        {
            "equipment_type": t.equipment_type,
            "number_equipment_type": t.number_equipment_type or [],
            "sub_equipment": t.sub_equipment or "",
            "number_sub_equipment": t.number_sub_equipment or []
        }
        for t in equipment_type
    ]