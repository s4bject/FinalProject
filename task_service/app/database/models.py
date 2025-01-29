from enum import Enum
from sqlalchemy import (
    Column, Date, Integer, String,
    ForeignKey, Enum as SQLEnum, Date, Table, func
)
from sqlalchemy.orm import relationship, validates, object_session

from .database import Base


class Grade(str, Enum):
    A = "a"
    B = "b"
    C = "c"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    worker_id = Column(Integer)
    task_manager_id = Column(Integer)
    date_create = Column(Date, nullable=False)
    commentary = Column(String)
    grade = Column(SQLEnum(Grade))
    deadline = Column(Date, nullable=False)


class Meet(Base):
    __tablename__ = "meets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    creator_id = Column(Integer, nullable=False)

    participants = relationship(
        "MeetParticipant",
        back_populates="meet",
        cascade="all, delete-orphan"
    )

    @validates('participants')
    def validate_availability(self, key, participant):
        session = object_session(self)
        if session:
            start_time = self.date
            end_time = func.datetime(self.date, f'+{self.duration} minutes')

            conflict = session.query(Meet).join(MeetParticipant).filter(
                MeetParticipant.user_id == participant.user_id,
                Meet.date < end_time,
                func.datetime(Meet.date, f'+{Meet.duration} minutes') > start_time
            ).first()

            if conflict:
                raise ValueError(f"Пользователь {participant.user_id} уже занят в это время!")
        return participant


class MeetParticipant(Base):
    __tablename__ = 'meet_participants'

    meet_id = Column(Integer, ForeignKey('meets.id'), primary_key=True)
    user_id = Column(Integer, nullable=False, primary_key=True)
    meet = relationship("Meet", back_populates="participants")
