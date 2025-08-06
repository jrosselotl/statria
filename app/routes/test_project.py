from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_project import TestProject
from app.schemas.test_project import TestProjectCreate, TestProjectOut

router = APIRouter(prefix="/test-project", tags=["Test Project"])

# Crear relación entre proyecto y tipo de test
@router.post("/", response_model=TestProjectOut)
def create_test_project(test_project: TestProjectCreate, db: Session = Depends(get_db)):
    db_obj = TestProject(**test_project.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Listar todos los test_project
@router.get("/", response_model=list[TestProjectOut])
def list_test_projects(db: Session = Depends(get_db)):
    return db.query(TestProject).all()

# Listar test_project por ID de proyecto
@router.get("/project/{project_id}", response_model=list[TestProjectOut])
def list_by_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(TestProject).filter_by(project_id=project_id).all()
