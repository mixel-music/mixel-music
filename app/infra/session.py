from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.sql import select, insert, update, delete
from core.models import Base
from tools.standard_path import *

DATABASE_URL = "sqlite:///" + database_url()
metadata = Base.metadata

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
db = Database(DATABASE_URL)

async def connect_database():
    await db.connect()
    await db.execute("PRAGMA journal_mode=WAL;")

async def disconnect_database():
    await db.disconnect()