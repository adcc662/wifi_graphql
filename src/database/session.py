from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.core.config import settings
from sqlalchemy import text

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Función para inicializar la base de datos
async def init_db():
    async with engine.begin() as conn:
        # Crear extensión PostGIS si no existe
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        # Crear todas las tablas
        await conn.run_sync(SQLModel.metadata.create_all)