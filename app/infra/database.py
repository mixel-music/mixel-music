from sqlalchemy import text, func, select, insert, update, delete
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.models import Base
from infra.config import *

engine = create_async_engine(conf.DB_URL, echo=conf.DB_ECHO)
session = sessionmaker(autoflush=False, bind=engine, class_=AsyncSession)
metadata = Base.metadata

async def connect_database():
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.run_sync(Base.metadata.create_all)

async def disconnect_database():
    await engine.dispose()