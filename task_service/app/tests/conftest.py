import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.execute.return_value = MagicMock()
    session.commit = AsyncMock()
    return session