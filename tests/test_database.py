import pytest
from sqlalchemy import text
from src.database.session import get_session


@pytest.mark.asyncio
async def test_database_connection():
    """Verify database connection"""
    session = await anext(get_session())
    try:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        await session.close()