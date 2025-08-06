from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.test_run import TestRun
from app.models.project import Project
from app.models.result_continuity import ResultContinuity
from app.models.result_insulation import ResultInsulation
from app.models.result_contact_resistance import ResultContactResistance
from app.models.result_torque import ResultTorque
from app.utils.pdf_generator import generate_test_pdf
from app.utils.email import send_email_with_pdf, get_admin_emails
import os
from datetime import datetime

router = APIRouter(prefix="/test_done", tags=["Test Done"])

@router.post("/send_pdf/{test_id}")
async def send_pdf(test_id: int, db: Session = Depends(get_db)):
    test_run = db.query(TestRun).filter(TestRun.id == test_id).first()
    if not test_run:
        raise HTTPException(status_code=404, detail="Test not found")

    project = db.query(Project).filter(Project.id == test_run.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    test_type = test_run.test_type.name
    MODEL_MAP = {
        "continuity": ResultContinuity,
        "insulation": ResultInsulation,
        "contact_resistance": ResultContactResistance,
        "torque": ResultTorque
    }
    ResultModel = MODEL_MAP.get(test_type)
    if not ResultModel:
        raise HTTPException(status_code=400, detail="Invalid test type")

    results = db.query(ResultModel).filter(ResultModel.test_run_id == test_id).all()
    if not results:
        raise HTTPException(status_code=400, detail="No results found for this test")

    equipment = test_run.equipment
    equipment_details = {
        "Project": project.name,
        "Main Location": f"{equipment.location_1} Nº{equipment.number_location_1}",
        "Secondary Location": (
            f"{equipment.location_2} Nº{equipment.number_location_2}" if equipment.location_2 else "-"
        ),
        "Equipment Type": f"{equipment.equipment_type} Nº{equipment.number_equipment_type}",
        "Sub Equipment": (
            f"{equipment.sub_equipment} Nº{equipment.number_sub_equipment}" if equipment.sub_equipment else "-"
        ),
        "Power Type": equipment.power_type,
        "Terminal": equipment.terminal
    }

    pdf_results = [
        {
            "cable_set": r.cable_set,
            "test_point": r.test_point,
            "result_value": r.result_value,
            "unit": r.unit,
            "observation": r.observations,
            "time_applied": getattr(r, "time_applied", None),
            "nominal_value": getattr(r, "nominal_value", None),
            "verification_value": getattr(r, "verification_value", None)
        }
        for r in results
    ]

    test_data = {
        "equipment_id": equipment.code,
        "test_type": test_type,
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "equipment_details": equipment_details,
        "images": [
            {"cable_set": r.cable_set, "test_point": r.test_point, "path": r.image_path}
            for r in results if r.image_path
        ],
        "user_name": test_run.user.full_name,
        "client_logo": project.client_logo,
        "subcontractor_logo": project.subcontractor_logo
    }

    pdf_path = f"output/{test_type}_{equipment.code}.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    generate_test_pdf(test_data, pdf_results, output_path=pdf_path)

    recipients = get_admin_emails(db, test_run.project_id)
    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients found to send the PDF.")

    send_email_with_pdf(
        recipients=recipients,
        subject=f"{test_type.capitalize()} - {equipment.code}",
        body=f"Test report for equipment {equipment.code}",
        pdf_file=pdf_path
    )

    return {"message": f"✅ PDF regenerated and sent successfully for test '{test_type.upper()}' ({equipment.code})"}
