from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.database import get_db
from passlib.context import CryptContext

router = APIRouter(prefix="/user", tags=["User"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create new user
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password_hash)
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_pw,
        role=user.role,
        company_id=user.company_id,
        is_active=user.is_active,
        user_mode=user.user_mode,
        registration_date=user.registration_date
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
@router.get("/", response_model=list[UserOut])
def list_user(db: Session = Depends(get_db)):
    return db.query(User).all()

# Reset password
@router.post("/reset-password")
def reset_password(
    email: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password_hash = pwd_context.hash(new_password)
    db.commit()
    return {"message": "Password updated successfully"}
