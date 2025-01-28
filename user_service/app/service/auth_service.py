from datetime import datetime, timedelta

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Company, Department


async def user_registration(db: AsyncSession, email: str, full_name: str, password: str, invite_code: str):
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже используется.")

    company, department = None, None

    if invite_code:
        company_code, department_code = invite_code.split("-")

        result = await db.execute(select(Company).where(Company.id == company_code))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=400, detail="Неверный инвайт-код.")

        result = await db.execute(
            select(Department).where(Department.id == department_code, Department.company_id == company.id))
        department = result.scalars().first()
        if not department:
            raise HTTPException(status_code=400, detail="Департамент не найден.")

    hashed_password = generate_password_hash(password)

    new_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        company_id=company.id if company else None,
        department_id=department.id if department else None,
        manager_id=department.department_head_id if department else None,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    if not check_password_hash(user.hashed_password, password):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    return user
