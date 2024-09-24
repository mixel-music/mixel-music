from sqlalchemy import text, func, select, insert, update, delete, or_, and_, join
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.sqlite import Insert
from contextlib import asynccontextmanager
from core.config import Config
from core.logging import *

Base = declarative_base()
engine = create_async_engine(Config.DBURL, echo=Config.DBECHO)
session = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@asynccontextmanager
async def db_conn():
    async with session() as conn:
        try:
            yield conn
            await conn.commit()
            
        except Exception as error:
            logs.error("Error occurred. %s", error)
            await conn.rollback()
            raise


async def connect_database() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.execute(text("PRAGMA busy_timeout=5000;"))
        await conn.run_sync(Base.metadata.create_all)


async def disconnect_database() -> None:
    await engine.dispose()
