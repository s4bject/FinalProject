from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, Enum as SQLEnum, Text
)
from sqlalchemy.orm import relationship

from .database import Base


class UserRole(str, Enum):
    REGULAR = "regular"
    DEPARTMENT_ADMIN = "department_admin"
    COMPANY_ADMIN = "company_admin"
    SUPER_ADMIN = "super_admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String())
    is_active = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole), default=UserRole.REGULAR)
    company_id = Column(Integer, ForeignKey("companies.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    admin_id = Column(Integer, ForeignKey("users.id"))


class CompanyAdmin(Base):
    __tablename__ = "company_admins"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"))
    department_head_id = Column(Integer, ForeignKey("users.id"))


class DepartmentAdmin(Base):
    __tablename__ = "department_admins"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"), primary_key=True)
