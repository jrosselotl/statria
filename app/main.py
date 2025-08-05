from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Base de datos
from app.database import get_db
from app.models.user import User

# Rutas
from app.routes import auth, log

# Inicializar app
app = FastAPI()

# Directorio base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Plantillas y estáticos
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Middleware de sesión
SESSION_SECRET = os.getenv("SESSION_SECRET_KEY", "w97k8Zj9B4fD1VmL3zXeT5GqNpHs0YuA")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# ============================
# 1️⃣ Página pública (landing)
# ============================
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("public/landing.html", {"request": request})

# =======================================================
# 2️⃣ Ruta común: redirección automática según el rol
# =======================================================
@app.get("/home", response_class=HTMLResponse)
async def home_redirect(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)
    
    if user.role == "project":
        return RedirectResponse(url="/admin", status_code=302)
    elif user.role == "technician":
        return RedirectResponse(url="/dashboard", status_code=302)
    elif user.role == "freelancer":
        return RedirectResponse(url="/freelancer", status_code=302)
    
    return RedirectResponse(url="/login", status_code=302)

# ======================================
# 3️⃣ Panel administrador para empresas
# ======================================
@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user or user.role != "project":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("project/index_admin.html", {"request": request})

# ===================================
# 4️⃣ Panel para técnicos internos
# ===================================
@app.get("/dashboard", response_class=HTMLResponse)
async def technician_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user or user.role != "technician":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("technician/dashboard.html", {"request": request})

# ====================================
# 5️⃣ Panel mixto para freelancers
# ====================================
@app.get("/freelancer", response_class=HTMLResponse)
async def freelancer_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user or user.role != "freelancer":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("freelancer/freelancer_dashboard.html", {"request": request})

# Incluir routers
app.include_router(auth.router)
app.include_router(log.router)
