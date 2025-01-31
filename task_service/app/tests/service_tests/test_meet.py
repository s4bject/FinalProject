import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from service.meet_service import create_meet, get_meets, delete_meet, update_meet
from schemas.schemas import MeetResponse, MeetUpdateRequest
from database.models import Meet, MeetParticipant


@pytest.mark.asyncio
async def test_create_meet_success(mock_session):
    mock_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None)))
    )

    mock_meet = Meet(
        id=1,
        name="Test Meet",
        date=date(2023, 1, 1),
        duration=60,
        creator_id=2,
        participants=[]
    )

    mock_session.add = MagicMock()
    mock_session.flush = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock(side_effect=lambda obj, _: setattr(obj, "id", 1))

    result = await create_meet(
        mock_session,
        "Test Meet",
        1,
        2,
        date(2023, 1, 1)
    )

    assert result.id == 1
    assert result.name == "Test Meet"
    assert result.creator_id == 2
    assert mock_session.add.call_count == 2
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_meet_conflict(mock_session):
    mock_meet = Meet(date=date(2023, 1, 1))
    mock_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_meet)))
    )

    with pytest.raises(HTTPException) as exc:
        await create_meet(
            mock_session,
            "Conflict Meet",
            1,
            2,
            date(2023, 1, 1)
        )

    assert exc.value.status_code == 400
    assert "уже имеет встречу" in exc.value.detail


@pytest.mark.asyncio
async def test_get_meets_success(mock_session):
    mock_meet = Meet(
        id=1,
        name="Test Meet",
        date=date(2023, 1, 1),
        duration=60,
        creator_id=1,
        participants=[MeetParticipant(user_id=1)]
    )
    mock_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[mock_meet])))
    )

    result = await get_meets(mock_session, 1)

    assert len(result) == 1
    assert result[0].name == "Test Meet"


@pytest.mark.asyncio
async def test_delete_meet_success(mock_session):
    mock_meet = Meet(id=1)
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=mock_meet)
    )

    await delete_meet(mock_session, 1)

    mock_session.delete.assert_called_once_with(mock_meet)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_meet_not_found(mock_session):
    mock_session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=None)
    )

    with pytest.raises(HTTPException) as exc:
        await delete_meet(mock_session, 999)

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_update_meet_name_success(mock_session):
    mock_meet = Meet(
        id=1,
        name="Old Name",
        date=date(2023, 1, 4),
        duration=60,
        creator_id=3,
        participants=[]
    )

    mock_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_meet)))
    )

    mock_session.commit = AsyncMock()

    result = await update_meet(mock_session, 1, "New Name", mock_meet.date, [])

    assert result.name == "New Name"
    assert result.date == mock_meet.date
    assert result.duration == 60
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_meet_conflict(mock_session):
    mock_meet = Meet(
        id=1,
        date=date(2023, 1, 1),
        participants=[MeetParticipant(user_id=1)]
    )
    conflict_meet = Meet(id=2)

    mock_session.execute.side_effect = [
        MagicMock(scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=mock_meet)))),
        MagicMock(scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=conflict_meet))))
    ]

    update_data = MeetUpdateRequest(
        name="Conflict Meet",
        date=date(2023, 1, 1),
        new_participants=[]
    )

    with pytest.raises(HTTPException) as exc:
        await update_meet(mock_session, 1, update_data.name, update_data.date, update_data.new_participants)

    assert exc.value.status_code == 400
    assert "уже занят" in exc.value.detail


@pytest.mark.asyncio
async def test_update_meet_not_found(mock_session):
    mock_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None)))
    )

    update_data = MeetUpdateRequest(
        name="Not Found",
        date=date(2023, 1, 1),
        new_participants=[]
    )

    with pytest.raises(HTTPException) as exc:
        await update_meet(mock_session, 999, update_data.name, update_data.date, update_data.new_participants)

    assert exc.value.status_code == 404
