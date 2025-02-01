from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Meet, MeetParticipant
from schemas.schemas import MeetResponse, MeetParticipantResponse, MeetUpdateRequest
from sqlalchemy.orm import selectinload, joinedload


async def create_meet(db: AsyncSession, name: str,
                      user_id: int, manag_id: int,
                      meet_date: date):
    query = (
        select(Meet)
        .join(MeetParticipant)
        .where(and_(MeetParticipant.user_id == user_id, Meet.date == meet_date))
    )
    result = await db.execute(query)
    existing_meet = result.scalars().first()

    if existing_meet:
        raise HTTPException(
            status_code=400,
            detail=f"Пользователь уже имеет встречу в этот день ({meet_date})"
        )

    new_meet = Meet(
        name=name,
        date=meet_date,
        duration=60,
        creator_id=manag_id
    )

    db.add(new_meet)
    await db.flush()

    participant = MeetParticipant(meet_id=new_meet.id, user_id=user_id)
    db.add(participant)

    try:
        await db.commit()
        await db.refresh(new_meet, ["participants"])
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка при добавлении встречи: {e}")

    return MeetResponse(
        id=new_meet.id,
        name=new_meet.name,
        date=new_meet.date,
        duration=new_meet.duration,
        creator_id=new_meet.creator_id,
        participants=[MeetParticipantResponse(user_id=p.user_id) for p in new_meet.participants]
    )


async def get_meets(db: AsyncSession, user_id: int):
    query = (
        select(Meet)
        .join(MeetParticipant)
        .where(MeetParticipant.user_id == user_id)
        .options(selectinload(Meet.participants))
    )
    result = await db.execute(query)
    meets = result.scalars().all()

    return meets


async def delete_meet(db: AsyncSession, meet_id: int):
    query = select(Meet).where(Meet.id == meet_id)
    result = await db.execute(query)
    meet = result.scalar_one_or_none()

    if not meet:
        raise HTTPException(status_code=404, detail="Встреча не найдена")

    await db.delete(meet)
    await db.commit()


async def update_meet(db: AsyncSession, meet_id: int, name: str, meet_date: date, new_participants: list[int]):
    query = select(Meet).options(joinedload(Meet.participants)).where(Meet.id == meet_id)
    result = await db.execute(query)
    meet = result.scalars().first()

    if not meet:
        raise HTTPException(status_code=404, detail="Встреча не найдена")

    for participant in meet.participants:
        query = (
            select(Meet)
            .join(MeetParticipant)
            .where(
                and_(
                    MeetParticipant.user_id == participant.user_id,
                    Meet.date == meet_date,
                    Meet.id != meet_id
                )
            )
        )
        result = await db.execute(query)
        conflicting_meet = result.scalars().first()

        if conflicting_meet:
            raise HTTPException(
                status_code=400,
                detail=f"Пользователь {participant.user_id} уже занят на встрече {conflicting_meet.id} в этот день ({meet_date})"
            )

    for user_id in new_participants:
        query = (
            select(Meet)
            .join(MeetParticipant)
            .where(
                and_(
                    MeetParticipant.user_id == user_id,
                    Meet.date == meet_date
                )
            )
        )
        result = await db.execute(query)
        conflicting_meet = result.scalars().first()

        if conflicting_meet:
            raise HTTPException(
                status_code=400,
                detail=f"Пользователь {user_id} уже занят на встрече {conflicting_meet.id} в этот день ({meet_date})"
            )

    meet.name = name
    meet.date = meet_date

    for user_id in new_participants:
        new_participant = MeetParticipant(meet_id=meet.id, user_id=user_id)
        db.add(new_participant)

    try:
        await db.commit()
        await db.refresh(meet, ["participants"])
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка при обновлении встречи: {e}")

    return MeetResponse(
        id=meet.id,
        name=meet.name,
        date=meet.date,
        duration=meet.duration,
        creator_id=meet.creator_id,
        participants=[MeetParticipantResponse(user_id=p.user_id) for p in meet.participants]
    )
