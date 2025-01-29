from datetime import date
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Grade(str, Enum):
    A = "a"
    B = "b"
    C = "c"


class TaskResponse(BaseModel):
    task: str
    worker_id: Optional[int] = None
    task_manager_id: Optional[int] = None
    date_create: date
    commentary: Optional[str] = None
    grade: Optional[Grade] = None
    deadline: date

    class Config:
        from_attributes = True


class TaskUpdateUser(BaseModel):
    commentary: Optional[str] = None

    class Config:
        from_attributes = True


class TaskUpdateAdmin(BaseModel):
    task: str
    worker_id: Optional[int] = None
    task_manager_id: Optional[int] = None
    commentary: Optional[str] = None
    grade: Optional[Grade] = None
    deadline: date


    class Config:
        from_attributes = True


class MeetParticipantResponse(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


class MeetResponse(BaseModel):
    name: str
    date: date
    duration: int
    creator_id: int
    participants: List[MeetParticipantResponse] = []

    class Config:
        from_attributes = True
