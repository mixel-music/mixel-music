from sqlalchemy import text, func, select, insert, update, delete
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.models import Base
from tools.standard_path import *

DATABASE_URL = "sqlite+aiosqlite:///" + database_url()
engine = create_async_engine(DATABASE_URL, echo=False)
session = sessionmaker(autoflush=False, bind=engine, class_=AsyncSession)
metadata = Base.metadata

async def connect_database():
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.run_sync(Base.metadata.create_all)

async def disconnect_database():
    await engine.dispose()

# from databases import Database
# from sqlalchemy import create_engine
# from sqlalchemy.sql import select, insert, update, delete

# DATABASE_URL = "sqlite+aiosqlite:///" + database_url()
# engine = create_async_engine(DATABASE_URL, echo=True)
# db = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# metadata = Base.metadata

# DATABASE_URL = "sqlite:///" + database_url()
# metadata = Base.metadata

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# metadata.create_all(engine)
# db = Database(DATABASE_URL)

# async def connect_database():
#     await db.connect()
#     await db.execute("PRAGMA journal_mode=WAL;")

# async def disconnect_database():
#     await db.disconnect()