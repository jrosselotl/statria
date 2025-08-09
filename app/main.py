from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# =============================
# 🔌 Base de datos y modelos
# =============================
from app.database import get_db
from app.models.user import User

# =============================
# ✅ Routers activos
# =============================
from app.routes import (
    auth,
    log,
    test_result_mapping,
    user,
    company,
    specialty,
    project,
    test_project,
    test_type,
    location,
    equipment_type,
    equipment,
    form,
    test_run,
    test_result_continuity,
    test_done,
    quality_certificate,
    certificate_assignment
)

# =============================
# 🚀 Inicializar la app
# =============================
app = FastAPI()

# =============================
# 🖼️ Archivos estáticos y templates
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# =============================
# 🔐 Middleware de sesión
# =============================
SESSION_SECRET = os.getenv("SESSION_SECRET_KEY", "clave_por_defecto_segura")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# =============================
# 🌐 Páginas principales (según rol)
# =============================

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("public/landing.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home_redirect(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login")
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login")
    
    match user.role:
        case "project": return RedirectResponse(url="/admin")
        case "technician": return RedirectResponse(url="/dashboard")
        case "freelancer": return RedirectResponse(url="/freelancer")
        case _: return RedirectResponse(url="/login")

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = db.query(User).filter_by(id=user_id).first() if user_id else None
    if not user or user.role != "project":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("project/index_admin.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def technician_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = db.query(User).filter_by(id=user_id).first() if user_id else None
    if not user or user.role != "technician":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("technician/dashboard.html", {"request": request})

@app.get("/freelancer", response_class=HTMLResponse)
async def freelancer_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = db.query(User).filter_by(id=user_id).first() if user_id else None
    if not user or user.role != "freelancer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("freelancer/freelancer_dashboard.html", {"request": request})

# =============================
# 🔁 Incluir rutas
# =============================

app.include_router(auth.router)
app.include_router(log.router)
app.include_router(user.router)
app.include_router(company.router)
app.include_router(specialty.router)
app.include_router(project.router)
app.include_router(test_project.router)
app.include_router(test_type.router)
app.include_router(location.router)
app.include_router(equipment_type.router)
app.include_router(equipment.router)
app.include_router(form.router)
app.include_router(test_run.router)
app.include_router(test_result_mapping.router)
app.include_router(test_result_continuity.router)
app.include_router(test_done.router)
app.include_router(quality_certificate.router)
app.include_router(certificate_assignment.router)
