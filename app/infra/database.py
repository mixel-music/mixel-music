from sqlalchemy import text, func, select, insert, update, delete, or_
from sqlalchemy.dialects.sqlite import Insert
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.models import Base
from infra.config import *

engine = create_async_engine(conf.DataBaseUrl, echo=conf.DataBaseEcho)
metadata = Base.metadata

session = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)

async def connect_database() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA busy_timeout=5000;"))
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_database() -> None:
    await engine.dispose()