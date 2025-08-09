from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_project import TestProject
from app.schemas.test_project import TestProjectCreate, TestProjectUpdate, TestProjectOut

router = APIRouter(prefix="/test_project", tags=["Test Project"])

@router.post("/", response_model=TestProjectOut)
def create_test_project(data: TestProjectCreate, db: Session = Depends(get_db)):
    new_entry = TestProject(**data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/", response_model=list[TestProjectOut])
def list_test_projects(db: Session = Depends(get_db)):
    return db.query(TestProject).all()

@router.get("/{test_project_id}", response_model=TestProjectOut)
def get_test_project(test_project_id: int, db: Session = Depends(get_db)):
    item = db.query(TestProject).filter_by(id=test_project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Test project not found")
    return item

@router.put("/{test_project_id}", response_model=TestProjectOut)
def update_test_project(test_project_id: int, data: TestProjectUpdate, db: Session = Depends(get_db)):
    item = db.query(TestProject).filter_by(id=test_project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Test project not found")
    for field, value in data.dict().items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{test_project_id}")
def delete_test_project(test_project_id: int, db: Session = Depends(get_db)):
    item = db.query(TestProject).filter_by(id=test_project_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Test project not found")
    db.delete(item)
    db.commit()
    return {"detail": "Test project deleted"}
