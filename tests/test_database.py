import pytest
from sqlalchemy import text
from src.database.session import get_session


@pytest.mark.asyncio
async def test_database_connection():
    """Verifica que la conexión a la base de datos funciona correctamente."""
    session = await anext(get_session())
    try:
        result = await session.execute(text("SELECT 1"))  # Envolver en `text()`
        assert result.scalar() == 1
    finally:
        await session.close()