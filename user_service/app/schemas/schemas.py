from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    REGULAR = "regular"
    COMPANY_ADMIN = "company_admin"
    SUPER_ADMIN = "super_admin"
    DEPARTMENT_ADMIN = "department_admin"


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    role: Optional[UserRole] = None
    company_id: Optional[int] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    is_active: bool
    email: EmailStr = Field(..., max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.REGULAR
    company_id: Optional[int] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None

    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    name: str = Field(..., max_length=100)


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int
    invite_code: str = Field(..., max_length=36)

    class Config:
        orm_mode = True


class CompanyAdminBase(BaseModel):
    user_id: int
    company_id: int


class CompanyAdminCreate(CompanyAdminBase):
    pass


class CompanyAdminResponse(CompanyAdminBase):
    class Config:
        orm_mode = True


class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    company_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        orm_mode = True


class InvitationBase(BaseModel):
    company_id: int


class InvitationCreate(InvitationBase):
    pass


class InvitationResponse(InvitationBase):
    id: int
    code: str = Field(..., max_length=36)
    used_by: Optional[int] = None

    class Config:
        orm_mode = True
