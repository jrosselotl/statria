from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.location import Location  # Updated model name

router = APIRouter(prefix="/location", tags=["Location"])

@router.get("/list")
def list_location(project_id: int, db: Session = Depends(get_db)):
    locations = db.query(Location).filter(Location.project_id == project_id).all()
    return [
        {
            "id": l.id,
            "location_1": l.location_1,
            "number_location_1": l.number_location_1 or [],
            "location_2": l.location_2,
            "number_location_2": l.number_location_2 or [],
        }
        for l in locations
    ]