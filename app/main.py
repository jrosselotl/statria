from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
import os

# Base de datos
from app.database import get_db
from app.models.user import User

# Rutas
from app.routes import auth

app = FastAPI()

# Directorio base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Plantillas y estáticos
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Middleware de sesión (obligatorio para login)
app.add_middleware(SessionMiddleware, secret_key="w97k8Zj9B4fD1VmL3zXeT5GqNpHs0YuA")

# Ruta protegida de inicio
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

    if user.role == "project":
        return RedirectResponse(url="/admin", status_code=302)

    return templates.TemplateResponse("index.html", {"request": request})

# Ruta protegida para usuarios "project"
@app.get("/admin", response_class=HTMLResponse)
async def read_admin(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter_by(id=user_id).first()
    if not user or user.role != "project":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("index_admin.html", {"request": request})

# Incluir rutas
app.include_router(auth.router)
