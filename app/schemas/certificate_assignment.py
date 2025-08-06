from pydantic import BaseModel

class CertificateAssignmentBase(BaseModel):
    quality_certificate_id: int
    test_type_id: int

class CertificateAssignmentCreate(CertificateAssignmentBase):
    pass

class CertificateAssignmentOut(CertificateAssignmentBase):
    id: int

    class Config:
        orm_mode = True
