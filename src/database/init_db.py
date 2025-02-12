# src/database/init_db.py
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import engine
from src.models.wifi_point import SQLModel

async def init_db():
    async with engine.begin() as conn:
        # Habilitar PostGIS
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        # Crear tablas
        await conn.run_sync(SQLModel.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())