from databases import Database
from .func import *
import sqlalchemy
import logging
import dotenv

DATABASE_URL = "sqlite:///" + str(get_absolute_path('data', 'tamaya.db'))
metadata = sqlalchemy.MetaData()

music = sqlalchemy.Table(
    "music",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("album", sqlalchemy.String),
    sqlalchemy.Column("artist", sqlalchemy.String),
    sqlalchemy.Column("year", sqlalchemy.String),
    sqlalchemy.Column("album_artist", sqlalchemy.String),
    sqlalchemy.Column("disc_number", sqlalchemy.Integer),
    sqlalchemy.Column("track_number", sqlalchemy.Integer),
    sqlalchemy.Column("is_compil", sqlalchemy.Boolean),
    sqlalchemy.Column("genre", sqlalchemy.String),
    sqlalchemy.Column("composer", sqlalchemy.String),
    sqlalchemy.Column("comment", sqlalchemy.String),
    sqlalchemy.Column("copyright", sqlalchemy.String),
    sqlalchemy.Column("isrc", sqlalchemy.String),
    sqlalchemy.Column("lyrics", sqlalchemy.String),
    sqlalchemy.Column("length", sqlalchemy.Integer),
    sqlalchemy.Column("bitrate", sqlalchemy.Integer),
    sqlalchemy.Column("channels", sqlalchemy.Integer),
    sqlalchemy.Column("sample_rate", sqlalchemy.Integer),
    sqlalchemy.Column("mime", sqlalchemy.String),
)

if not get_absolute_path('data', 'tamaya.db').exists():
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    logging.debug("Creating DB Tables...")
    database = Database(DATABASE_URL)
else:
    database = Database(DATABASE_URL)

async def connect_database():
    await database.connect()

async def disconnect_database():
    await database.disconnect()