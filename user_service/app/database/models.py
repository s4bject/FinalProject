from enum import Enum
from sqlalchemy import (
    Column, Date, Integer, String, Boolean,
    ForeignKey, Enum as SQLEnum, Text
)
from sqlalchemy.orm import relationship, Mapped

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
    role = Column(SQLEnum(UserRole), default=UserRole.SUPER_ADMIN)
    company_id = Column(Integer, ForeignKey("companies.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))

    company = relationship(
        "Company",
        back_populates="users",
        foreign_keys=[company_id]
    )
    department = relationship(
        "Department",
        back_populates="users",
        foreign_keys=[department_id]
    )
    manager = relationship(
        "User",
        remote_side=[id],
        back_populates="subordinates",
        foreign_keys=[manager_id]
    )
    subordinates = relationship("User", back_populates="manager")
    administered_company = relationship(
        "Company",
        back_populates="admin",
        foreign_keys="Company.admin_id",
        uselist=False
    )
    administered_departments = relationship(
        "Department",
        back_populates="department_head",
        foreign_keys="Department.department_head_id"
    )

    def __repr__(self):
        return f"<User {self.id}: {self.email}, {self.full_name}>"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"))

    users = relationship(
        "User",
        back_populates="company",
        foreign_keys="User.company_id"
    )
    departments = relationship(
        "Department",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    admin = relationship(
        "User",
        back_populates="administered_company",
        foreign_keys=[admin_id]
    )

    def __repr__(self):
        return f"<Company {self.id}: {self.name}. Admin - {self.admin_id}>"


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"))
    department_head_id = Column(Integer, ForeignKey("users.id"))

    company = relationship(
        "Company",
        back_populates="departments",
        foreign_keys=[company_id]
    )
    users = relationship(
        "User",
        back_populates="department",
        foreign_keys="User.department_id"
    )
    department_head = relationship(
        "User",
        back_populates="administered_departments",
        foreign_keys=[department_head_id]
    )

    def __repr__(self):
        return f"<Department {self.id}: {self.name} (Company {self.company_id} Admin - {self.department_head_id})>"


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    head = Column(String(250))
    description = Column(Text)
    date_create = Column(Date)
