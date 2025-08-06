from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Para recibir datos al crear usuario
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password_hash: str  # Este campo es la contraseña en texto plano, luego se hashea
    role: str
    company_id: Optional[int]
    is_active: Optional[bool] = True
    user_mode: Optional[str] = "internal"
    registration_date: Optional[datetime] = None

# Para mostrar datos al frontend (sin contraseña)
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    company_id: Optional[int]
    is_active: bool
    user_mode: Optional[str]
    registration_date: Optional[datetime]

    class Config:
        orm_mode = True
