from databases import Database
from .path import *
import sqlalchemy
import logging

db_abs_path = PathTool.abs_path('conf', 'tamaya.db')
db_abs_path_str = db_abs_path.as_posix()

DATABASE_URL = "sqlite:///" + db_abs_path_str
metadata = sqlalchemy.MetaData()

music = sqlalchemy.Table(
    "music",
    metadata,
    sqlalchemy.Column("album", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("album_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("album_sort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("album_artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("album_artist_sort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist_sort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("barcode", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("bitrate", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("bpm", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("catalog_number", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("channels", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("comment", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("compilation", sqlalchemy.Boolean(False), nullable=False),
    sqlalchemy.Column("composer", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("composer_sort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("conductor", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("content_group", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("copyright", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("date", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("disc_number", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("duration", sqlalchemy.REAL, nullable=False),
    sqlalchemy.Column("genre", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("grouping", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("id", sqlalchemy.String(''), nullable=False, primary_key=True),
    sqlalchemy.Column("involved_people", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("isrc", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("language", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("lyricist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("lyrics", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("mime", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("mix_artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_album_artist_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_album_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_album_type", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_artist_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_disc_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_original_album_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_original_artist_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_release_group_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_release_track_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_track_id", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("orignal_album", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("orignal_artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("orignal_lyricist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("orignal_year", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("path", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("publisher", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("release_time", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("sample_rate", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("set_subtitle", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("subtitle", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("title_sort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("track_number", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("update_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("year", sqlalchemy.Integer, nullable=False),
)

if not db_abs_path.exists():
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    database = Database(DATABASE_URL)
    logging.debug("Database not found. creating...")
else:
    database = Database(DATABASE_URL)

async def connect_database():
    await database.connect()

async def disconnect_database():
    await database.disconnect()