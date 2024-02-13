from databases import Database
from .func import *
import sqlalchemy
import logging
import dotenv

DATABASE_URL = "sqlite:///" + str(get_absolute_path('data', 'tamaya.db'))
metadata = sqlalchemy.MetaData()

# music = sqlalchemy.Table(
#     "music",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
#     sqlalchemy.Column("title", sqlalchemy.String),
#     sqlalchemy.Column("album", sqlalchemy.String),
#     sqlalchemy.Column("artist", sqlalchemy.String),
#     sqlalchemy.Column("year", sqlalchemy.String),
#     sqlalchemy.Column("album_artist", sqlalchemy.String),
#     sqlalchemy.Column("disc_number", sqlalchemy.Integer),
#     sqlalchemy.Column("track_number", sqlalchemy.Integer),
#     sqlalchemy.Column("is_compil", sqlalchemy.Boolean),
#     sqlalchemy.Column("genre", sqlalchemy.String),
#     sqlalchemy.Column("composer", sqlalchemy.String),
#     sqlalchemy.Column("comment", sqlalchemy.String),
#     sqlalchemy.Column("copyright", sqlalchemy.String),
#     sqlalchemy.Column("isrc", sqlalchemy.String),
#     sqlalchemy.Column("lyrics", sqlalchemy.String),
#     sqlalchemy.Column("length", sqlalchemy.Integer),
#     sqlalchemy.Column("bitrate", sqlalchemy.Integer),
#     sqlalchemy.Column("channels", sqlalchemy.Integer),
#     sqlalchemy.Column("sample_rate", sqlalchemy.Integer),
#     sqlalchemy.Column("mime", sqlalchemy.String),
# )

music = sqlalchemy.Table(
    "music",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("album", sqlalchemy.String),
    sqlalchemy.Column("artist", sqlalchemy.String),
    sqlalchemy.Column("year", sqlalchemy.String),
    sqlalchemy.Column("album_artist", sqlalchemy.String),
    sqlalchemy.Column("disc_number", sqlalchemy.String),
    sqlalchemy.Column("track_number", sqlalchemy.String),
    sqlalchemy.Column("is_compil", sqlalchemy.String),
    sqlalchemy.Column("genre", sqlalchemy.String),
    sqlalchemy.Column("composer", sqlalchemy.String),
    sqlalchemy.Column("comment", sqlalchemy.String),
    sqlalchemy.Column("copyright", sqlalchemy.String),
    sqlalchemy.Column("isrc", sqlalchemy.String),
    sqlalchemy.Column("lyrics", sqlalchemy.String),
    sqlalchemy.Column("length", sqlalchemy.String),
    sqlalchemy.Column("bitrate", sqlalchemy.String),
    sqlalchemy.Column("channels", sqlalchemy.String),
    sqlalchemy.Column("sample_rate", sqlalchemy.String),
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

async def insert_music(
    id: str = '',
    title: str = '',
    album: str = '',
    artist: str = '',
    year: str = '',
    album_artist: str = '',
    disc_number: str = '',
    track_number: str = '',
    is_compil: str = '',
    genre: str = '',
    composer: str = '',
    comment: str = '',
    copyright: str = '',
    isrc: str = '',
    lyrics: str = '',
    length: str = '',
    bitrate: str = '',
    channels: str = '',
    sample_rate: str = '',
    mime: str = ''
    ):
    """
    Insert music tags into DB, all values are String for prevent exception (DEBUG)
    """

    query = music.insert().values(
        id=id,
        title=title,
        album=album,
        artist=artist,
        year=year,
        album_artist=album_artist,
        disc_number=disc_number,
        track_number=track_number,
        is_compil=is_compil,
        genre=genre,
        composer=composer,
        comment=comment,
        copyright=copyright,
        isrc=isrc,
        lyrics=lyrics,
        length=length,
        bitrate=bitrate,
        channels=channels,
        sample_rate=sample_rate,
        mime=mime
    )

    await database.execute(query)
    logging.debug("music data insert completed, id = %s, title = %s", str(id), str(title))

async def update_music():
    return None

async def delete_music():
    return None

async def processing_cover_image():
    return None