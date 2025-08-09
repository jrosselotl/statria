from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.project import Project
from app.models.test_type import TestType
from app.models.equipment import Equipment
from app.models.test_run import TestRun
from app.models.test_result_continuity import TestResultContinuity
from app.models.test_result_insulation import TestResultInsulation
from app.models.test_result_contact_resistance import TestResultContactResistance
from app.models.test_result_torque import TestResultTorque
from app.routes.auth import get_current_user
from app.models.user import User
import os
import shutil
from datetime import datetime
import json

router = APIRouter(prefix="/form", tags=["Form"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/save")
async def save_form(
    request: Request,
    project_id: int = Form(...),
    location_1: str = Form(...),
    number_location_1: int = Form(...),
    location_2: Optional[str] = Form(None),
    number_location_2: Optional[int] = Form(None),
    equipment_type: str = Form(...),
    number_equipment_type: Optional[int] = Form(None),
    sub_equipment: Optional[str] = Form(None),
    number_sub_equipment: Optional[int] = Form(None),

    # 👇 llega en snake_case desde el select (lo seguimos aceptando)
    test_type: str = Form(...),
    # 👇 NUEVO: ID real del test (lo preferimos)
    test_type_id: Optional[int] = Form(None),

    cable_set: int = Form(...),
    power_type: str = Form(...),
    terminal: Optional[str] = Form(None),
    unit: Optional[str] = Form(None),
    data: str = Form(...),
    images: Optional[list[UploadFile]] = File(None),
    completed: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = current_user.id

    # Normaliza None
    location_2 = location_2 or None
    number_location_2 = number_location_2 or None
    sub_equipment = sub_equipment or None
    number_sub_equipment = number_sub_equipment or None

    # ---- Equipment code
    parts = [f"{location_1}{number_location_1}"]
    if location_2 and number_location_2:
        parts.append(f"{location_2}{number_location_2}")
    if number_equipment_type is not None:
        parts.append(f"{equipment_type}{number_equipment_type}")
    else:
        parts.append(f"{equipment_type}")
    if sub_equipment and number_sub_equipment:
        parts.append(f"{sub_equipment}{number_sub_equipment}")
    equipment_code = "-".join(parts).upper()

    equipment = db.query(Equipment).filter(Equipment.code == equipment_code).first()
    if not equipment:
        equipment = Equipment(
            project_id=project_id,
            location_1=location_1,
            number_location_1=number_location_1,
            location_2=location_2,
            number_location_2=number_location_2,
            equipment_type=equipment_type,
            number_equipment_type=number_equipment_type,
            sub_equipment=sub_equipment,
            number_sub_equipment=number_sub_equipment,
            terminal=terminal,
            power_type=power_type,
            cable_set=cable_set,
            code=equipment_code
        )
        db.add(equipment)
        db.commit()
        db.refresh(equipment)

    # ---- Resolver TestType
    from sqlalchemy import func
    test_type_obj = None
    if test_type_id:
        test_type_obj = db.query(TestType).filter(TestType.id == test_type_id).first()
    if not test_type_obj:
        # fallback: del snake_case a nombre "Contact Resistance"
        human = test_type.replace("_", " ").strip()
        test_type_obj = (
            db.query(TestType)
              .filter(func.lower(TestType.name) == func.lower(human))
              .first()
        )

    if not test_type_obj:
        raise HTTPException(status_code=400, detail=f"Test type '{test_type}' not found")

    # ---- TestRun
    test_run = (
        db.query(TestRun)
          .filter(TestRun.equipment_id == equipment.id,
                  TestRun.test_type_id == test_type_obj.id)
          .first()
    )
    if not test_run:
        test_run = TestRun(
            project_id=project_id,
            equipment_id=equipment.id,
            user_id=user_id,
            test_type_id=test_type_obj.id,
            status="incomplete"
        )
        db.add(test_run)
        db.commit()
        db.refresh(test_run)

    # ---- Parse data
    try:
        data_parsed = json.loads(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid data format")

    all_filled = all(
        (r.get("result_value") is not None and r.get("result_value") != "")
        or r.get("result_value") == "N/A"
        for r in data_parsed
    )
    test_run.status = "completed" if completed and all_filled else "incomplete"

    # ---- Persist results
    MODEL_MAP = {
        "continuity": TestResultContinuity,
        "insulation": TestResultInsulation,
        "contact_resistance": TestResultContactResistance,
        "torque": TestResultTorque
    }
    ResultModel = MODEL_MAP.get(test_type)
    if not ResultModel:
        raise HTTPException(status_code=400, detail="Invalid test type")

    db.query(ResultModel).filter(ResultModel.test_run_id == test_run.id).delete()

    img_iter = iter(images or [])
    for r in data_parsed:
        image = next(img_iter, None)
        path = None
        if image and image.filename:
            filename = f"{datetime.utcnow().timestamp()}_{image.filename}"
            path = os.path.join(UPLOAD_DIR, filename)
            with open(path, "wb") as f:
                shutil.copyfileobj(image.file, f)

        result_data = {
            "test_run_id": test_run.id,
            "test_point": r["test_point"],
            "unit": r.get("unit") or unit,
            "observations": r.get("observation", ""),
            "image_path": path if path else None,
            "cable_set": r.get("cable_set")
        }

        if test_type in ["continuity", "contact_resistance", "insulation"]:
            result_data["result_value"] = (
                None if r.get("result_value") == "N/A" else r.get("result_value")
            )
        if test_type == "insulation":
            result_data["time_applied"] = r.get("time_applied")
        if test_type == "torque":
            result_data["nominal_value"] = r.get("nominal_value")
            result_data["verification_value"] = r.get("verification_value")

        db.add(ResultModel(**result_data))

    db.commit()

    return {
        "message": f"✅ Test {'completed' if test_run.status == 'completed' else 'saved as draft'} successfully",
        "test_id": test_run.id
    }

@router.get("/load_test/{test_id}")
async def load_test(test_id: int, db: Session = Depends(get_db)):
    test_run = db.query(TestRun).filter(TestRun.id == test_id).first()
    if not test_run:
        raise HTTPException(status_code=404, detail="Test not found")

    test_type = test_run.test_type.name
    MODEL_MAP = {
        "continuity": TestResultContinuity,
        "insulation": TestResultInsulation,
        "contact_resistance": TestResultContactResistance,
        "torque": TestResultTorque
    }
    ResultModel = MODEL_MAP.get(test_type)
    if not ResultModel:
        raise HTTPException(status_code=400, detail="Invalid test type")

    results = db.query(ResultModel).filter(ResultModel.test_run_id == test_id).all()

    response_results = []
    for r in results:
        base = {
            "cable_set": r.cable_set,
            "test_point": r.test_point,
            "result_value": r.result_value,
            "observation": r.observations,
            "unit": r.unit
        }
        if test_type == "insulation":
            base["time_applied"] = getattr(r, "time_applied", None)
        if test_type == "torque":
            base["nominal_value"] = getattr(r, "nominal_value", None)
            base["verification_value"] = getattr(r, "verification_value", None)
        response_results.append(base)

    return {
        "project_id": test_run.project_id,
        "test_type": test_type,
        "results": response_results
    }
