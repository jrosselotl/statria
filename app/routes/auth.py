from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.utils.logger import logger
import os
# Models
from app.database import get_db
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Login page
@router.get("/login", response_class=HTMLResponse)
def show_login(request: Request):
    print("Files in auth/", os.listdir("app/templates/auth"))
    return templates.TemplateResponse("auth/login.html", {"request": request})

# Process login
@router.post("/auth/login")
def process_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=email).first()

    if not user or not pwd_context.verify(password, user.password_hash):
        logger.warning(f"Login failed for email: {email}")
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Credenciales incorrectas"}
        )

    logger.info(f"User {user.email} logged in successfully.")

    # Guardar sesión
    request.session["user_id"] = user.id
    request.session["user_role"] = user.role
    if remember:
        request.session["remember"] = True

    # Redirección por rol
    if user.role == "project":
        return RedirectResponse(url="/admin", status_code=HTTP_302_FOUND)
    elif user.role == "technician":
        return RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)
    elif user.role == "freelancer":
        return RedirectResponse(url="/freelancer", status_code=HTTP_302_FOUND)
    else:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Rol no reconocido"}
        )

# Logout
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

# Get current user (para proteger rutas)
def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
