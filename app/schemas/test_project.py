from pydantic import BaseModel


class TestProjectBase(BaseModel):
    project_id: int
    test_type_id: int
    is_enabled: bool = True
    active: bool = True

    class Config:
        from_attributes = True  # En Pydantic v2 reemplaza orm_mode


class TestProjectCreate(TestProjectBase):
    pass


class TestProjectUpdate(BaseModel):
    is_enabled: bool | None = None
    active: bool | None = None

    class Config:
        from_attributes = True


class TestProjectOut(TestProjectBase):
    id: int

    class Config:
        from_attributes = True
