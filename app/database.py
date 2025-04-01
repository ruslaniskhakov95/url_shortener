import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from typing import AsyncGenerator
sys.path.append(
    str(Path(__file__).parent.parent)
)
from app.config import PG_USER, PG_PASS, PG_DB, HOST, PORT


DB_URL = f'postgresql+asyncpg://{PG_USER}:{PG_PASS}@{HOST}:{PORT}/{PG_DB}'

engine = create_async_engine(
    DB_URL,
    echo=True,
    future=True,
    pool_size=10,
    max_overflow=20
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
