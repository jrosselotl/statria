from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import datetime
import shutil, os, json

from app.database import get_db
from app.models.test_run import TestRun
from app.models.equipment import Equipment
from app.models.test_type import TestType
from app.models.test_project import TestProject

# ✅ Result models
from app.models.result_continuity import ResultContinuity
from app.models.result_insulation import ResultInsulation
from app.models.result_contact_resistance import ResultContactResistance
from app.models.result_torque import ResultTorque

router = APIRouter(prefix="/test_run", tags=["Test Run"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ 1. Crear test_run + resultados
@router.post("/create")
async def create_test_run(request: Request, db: Session = Depends(get_db)):
    """
    Recibe FormData:
    - project_id, equipment_id, user_id, test_type_id, certificate_id
    - general_image, general_images
    - results (JSON string)
    - Imágenes con nombre image_${i}_${point}
    """
    form = await request.form()
    try:
        project_id = int(form["project_id"])
        equipment_id = int(form["equipment_id"])
        user_id = int(form["user_id"])
        test_type_id = int(form["test_type_id"])
        certificate_id = int(form["certificate_id"]) if form.get("certificate_id") else None

        general_image = form.get("general_image")
        general_images = form.get("general_images")

        new_test = TestRun(
            project_id=project_id,
            equipment_id=equipment_id,
            user_id=user_id,
            test_type_id=test_type_id,
            certificate_id=certificate_id,
            general_image=general_image,
            general_images=general_images,
            started_at=datetime.utcnow(),
        )

        db.add(new_test)
        db.flush()

        results = json.loads(form["results"])
        test_type = db.query(TestType).filter(TestType.id == test_type_id).first().name.lower()

        for r in results:
            image_field = r.get("image_field")
            image_file = form.get(image_field)
            image_path = None

            if image_file and hasattr(image_file, "filename") and image_file.filename:
                filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image_file.filename}"
                file_location = os.path.join(UPLOAD_DIR, filename)
                with open(file_location, "wb") as f:
                    shutil.copyfileobj(image_file.file, f)
                image_path = f"/{file_location}"

            common_data = {
                "test_run_id": new_test.id,
                "test_point": r["test_point"],
                "observation": r.get("observation"),
                "cable_set": r.get("cable_set"),
                "image_url": image_path,
                "unit": r.get("unit")
            }

            if test_type == "continuity":
                db.add(ResultContinuity(**common_data, result_value=r.get("result_value")))
            elif test_type == "insulation":
                db.add(ResultInsulation(**common_data, result_value=r.get("result_value"), time_applied=r.get("time_applied")))
            elif test_type == "contact_resistance":
                db.add(ResultContactResistance(**common_data, result_value=r.get("result_value")))
            elif test_type == "torque":
                db.add(ResultTorque(**common_data, nominal_value=r.get("nominal_value"), verification_value=r.get("verification_value")))

        db.commit()
        return {"message": f"✅ TestRun creado con ID {new_test.id}"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Error al crear TestRun: {str(e)}")


# ✅ 2. Listar tests por usuario
@router.get("/list_user/{user_id}")
def list_user_tests(user_id: int, db: Session = Depends(get_db)):
    tests = (
        db.query(TestRun, Equipment, TestType)
        .join(Equipment, TestRun.equipment_id == Equipment.id)
        .join(TestType, TestRun.test_type_id == TestType.id)
        .filter(TestRun.user_id == user_id)
        .order_by(TestRun.started_at.desc())
        .all()
    )

    return [
        {
            "id": t.TestRun.id,
            "test_type": t.TestType.name,
            "asset": "-".join(
                filter(
                    None,
                    [
                        f"{t.Equipment.location_1}{t.Equipment.number_location_1 or ''}",
                        f"{t.Equipment.location_2}{t.Equipment.number_location_2 or ''}" if t.Equipment.location_2 else None,
                        f"{t.Equipment.equipment_type}{t.Equipment.number_equipment_type or ''}",
                        f"{t.Equipment.sub_equipment}{t.Equipment.number_sub_equipment or ''}" if t.Equipment.sub_equipment else None,
                    ],
                )
            ),
            "date": t.TestRun.started_at.strftime("%Y-%m-%d"),
        }
        for t in tests
    ]


# ✅ 3. Stats por usuario y proyecto
@router.get("/list_user_stats/{user_id}")
def list_user_stats(user_id: int, project_id: int, db: Session = Depends(get_db)):
    assigned_tests = (
        db.query(TestType)
        .join(TestProject, TestProject.test_type_id == TestType.id)
        .filter(TestProject.project_id == project_id, TestProject.active == True)
        .all()
    )

    if not assigned_tests:
        raise HTTPException(status_code=404, detail="No hay tests asignados a este proyecto")

    results = {}
    for test in assigned_tests:
        total = (
            db.query(TestRun)
            .filter(
                TestRun.test_type_id == test_type.id,
                TestRun.project_id == project_id,
                TestRun.user_id == user_id
            )
            .count()
        )
        results[test.name] = total

    return results
