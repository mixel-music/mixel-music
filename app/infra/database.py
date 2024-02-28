from infra.path_handler import *
from infra.setup_logger import *
from databases import Database
import sqlalchemy

DATABASE_URL = "sqlite:///" + database_url()
metadata = sqlalchemy.MetaData()
tracks = sqlalchemy.Table(
    "tracks",
    metadata,
    sqlalchemy.Column("album", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumartist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumartistsort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumsort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artistid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artists", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artistsort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("barcode", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("bitrate", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("bpm", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("catalognumber", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("channels", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("comment", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("compilation", sqlalchemy.Boolean(False), nullable=False),
    sqlalchemy.Column("composer", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("composersort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("conductor", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("contentgroup", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("copyright", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("create_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("date", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("director", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("directory", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("discnumber", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("disctotal", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("duration", sqlalchemy.REAL, nullable=False),
    sqlalchemy.Column("genre", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("grouping", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("id", sqlalchemy.String(''), nullable=False, primary_key=True),
    sqlalchemy.Column("imageid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("isrc", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("label", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("language", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("lyricist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("lyrics", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("media", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("mediatype", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("mime", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("mixartist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_albumartistid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_albumid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_albumreleasecountry", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_albumstatus", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_albumtype", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_artistid", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("musicbrainz_discid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_originalalbumid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_originalartistid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_releasegroupid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_releasetrackid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("musicbrainz_trackid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("organization", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("origalbum", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("origartist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("originaldate", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("originalyear", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("origlyricist", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("origyear", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("path", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("releasestatus", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("releasetype", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("samplerate", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("script", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("setsubtitle", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("subtitle", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("titlesort", sqlalchemy.String(''), nullable=False),
    # sqlalchemy.Column("track", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("tracknumber", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("tracktotal", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("update_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("year", sqlalchemy.Integer, nullable=False),
)
albums = sqlalchemy.Table(
    "albums",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumartist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("albumid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("disctotal", sqlalchemy.Integer, nullable=False), #
    sqlalchemy.Column("duration", sqlalchemy.REAL, nullable=False),
    sqlalchemy.Column("image_path", sqlalchemy.Integer, nullable=False), #
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("tracknumber", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("year_new", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("year_old", sqlalchemy.Integer, nullable=False),
)
artists = sqlalchemy.Table(
    "artists",
    metadata,
    sqlalchemy.Column("artist", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artistid", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artists", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("artistsort", sqlalchemy.String(''), nullable=False),
    sqlalchemy.Column("duration", sqlalchemy.REAL, nullable=False),
    sqlalchemy.Column("image_path", sqlalchemy.Integer, nullable=False), #
    sqlalchemy.Column("size", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("tracknumber", sqlalchemy.Integer, nullable=False),
)

if not get_path(database_url()).exists():
    logs.info("Creating new database...")
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

    metadata.create_all(engine)
    db = Database(DATABASE_URL)
else:
    db = Database(DATABASE_URL)

async def connect_database():
    await db.connect()
    await db.execute("PRAGMA journal_mode=WAL;")
    logs.info("Connected to database successfully.")

async def disconnect_database():
    await db.disconnect()