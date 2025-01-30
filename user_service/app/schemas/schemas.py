from datetime import date

from pydantic import BaseModel, EmailStr, Field, constr
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
    role: Optional[UserRole] = None
    company_id: Optional[int] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr = Field(..., max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.REGULAR
    company_id: Optional[int] = None
    manager_id: Optional[int] = None
    department_id: Optional[int] = None

    class Config:
        from_attributes = True


class NewsResponse(BaseModel):
    id: int
    head: constr(max_length=250)
    description: str
    date_create: date

    class Config:
        from_attributes = True


class ExternalMeetUpdateRequest(BaseModel):
    meet_id: int
    name: str
    date: str
    new_participants: list[int]
