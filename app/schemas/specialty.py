from pydantic import BaseModel

class SpecialtyBase(BaseModel):
    name: str

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyUpdate(SpecialtyBase):
    pass

class SpecialtyOut(SpecialtyBase):
    id: int

    class Config:
        orm_mode = True
