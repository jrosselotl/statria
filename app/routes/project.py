from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.project import Project
from app.models.test_project import TestProject   # ver modelo más abajo
from app.models.test_type import TestType         # para validar existencia
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectOut,
    TestProjectBase, TestProjectOut
)

router = APIRouter(prefix="/project", tags=["Project"])

# -------- CRUD Project --------
@router.post("/", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    exists = db.query(Project).filter(Project.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Project name already exists")

    obj = Project(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[ProjectOut])
def list_project(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.id.asc()).all()

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.query(Project).get(project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    obj = db.query(Project).get(project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.query(Project).get(project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(obj)
    db.commit()
    return {"message": "Project deleted"}

# -------- Asignación de tipos de test al proyecto --------
@router.post("/{project_id}/test-type", response_model=TestProjectOut)
def add_test_type_to_project(project_id: int, payload: TestProjectBase, db: Session = Depends(get_db)):
    # valida proyecto y tipo
    if not db.query(Project).get(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    if not db.query(TestType).get(payload.test_type_id):
        raise HTTPException(status_code=404, detail="Test type not found")

    rel = db.query(TestProject).filter(
        TestProject.project_id == project_id,
        TestProject.test_type_id == payload.test_type_id
    ).first()

    if rel:
        # si ya existe, solo actualiza 'active'
        rel.active = payload.active
    else:
        rel = TestProject(project_id=project_id,
                          test_type_id=payload.test_type_id,
                          active=payload.active)
        db.add(rel)

    db.commit()
    db.refresh(rel)
    return rel

@router.get("/{project_id}/test-type", response_model=List[TestProjectOut])
def list_project_test_types(project_id: int, db: Session = Depends(get_db)):
    if not db.query(Project).get(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(TestProject).filter(TestProject.project_id == project_id).all()

@router.delete("/{project_id}/test-type/{test_type_id}")
def remove_test_type_from_project(project_id: int, test_type_id: int, db: Session = Depends(get_db)):
    rel = db.query(TestProject).filter(
        TestProject.project_id == project_id,
        TestProject.test_type_id == test_type_id
    ).first()
    if not rel:
        raise HTTPException(status_code=404, detail="Relation not found")
    db.delete(rel)
    db.commit()
    return {"message": "Relation removed"}
