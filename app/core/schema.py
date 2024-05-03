from pydantic import BaseModel, create_model
from sqlalchemy import inspect
from datetime import datetime
from core.models import *

def sql_schema(sql_class):
    inspector = inspect(sql_class)
    attributes = {}

    for column in inspector.c:
        attributes[column.name] = (column.type.python_type, None)

    return create_model(sql_class.__name__, **attributes)

class TrackSchema(sql_schema(Tracks)):
    pass

class TrackListSchema(BaseModel):
    hash: str = None
    title: str = None
    album: str = None
    albumhash: str = None
    artist: str = None
    artisthash: str = None
    created_date: datetime = None
    updated_date: datetime = None
    imagehash: str = None
    date: str = None
    year: int = None
    genre: str = None
    musicbrainz_trackid: str = None

    class Config:
        from_attributes = True

class AlbumSchema(sql_schema(Albums)):
    tracks: list = None

class AlbumListSchema(BaseModel):
    albumhash: str = None
    album: str = None
    albumartist: str = None
    imagehash: str = None
    year: int = None
    tracktotals: int = None
    disctotals: int = None

    class Config:
        from_attributes = True

class ArtistSchema(sql_schema(Artists)):
    pass

class ArtistListSchema(BaseModel):
    artisthash: str = None
    artist: str = None
    imagehash: str = None

    class Config:
        from_attributes = True