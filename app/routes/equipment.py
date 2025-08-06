from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.equipment import EquipmentCreate, EquipmentOut
from app.models.equipment import Equipment
from app.database import get_db

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.post("/", response_model=EquipmentOut)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    # Validar que no exista un equipo con el mismo código
    existing = db.query(Equipment).filter(Equipment.code == equipment.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Code already exists")

    new_equipment = Equipment(**equipment.dict())
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment


@router.get("/list", response_model=list[EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(Equipment).all()
