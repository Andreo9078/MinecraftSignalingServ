from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.config import DB_NAME

DATA_BASE_URL = f"sqlite+aiosqlite:///{DB_NAME}"


class Base(DeclarativeBase, AsyncAttrs):
    pass


engine = create_async_engine(DATA_BASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
