from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from tools.path_handler import *
from datetime import datetime
import logging

class Tracks(BaseModel):
    hash: str = Field(default=None, example="test")
    title: str = Field(default=None)
    artist: str = Field(default=None)
    artisthash: str = Field(default=None)
    album: str = Field(default=None)
    albumhash: str = Field(default=None)
    albumartist: str = Field(default=None)
    bitdepth: int = Field(default=None)
    bitrate: float = Field(default=None)
    channels: int = Field(default=None)
    comment: str = Field(default=None)
    composer: str = Field(default=None)
    disc: int = Field(default=None)
    disctotal: int = Field(default=None)
    duration: float = Field(default=None)
    size: int = Field(default=None)
    genre: str = Field(default=None)
    samplerate: int = Field(default=None)
    track: int = Field(default=None)
    tracktotal: int = Field(default=None)
    year: str = Field(default=None)
    directory: str = Field(default=None)
    mime: str = Field(default=None)
    path: str = Field(default=None)
    created_date: datetime = Field(default=None)
    updated_date: datetime = Field(default=None)
    unsyncedlyrics: str = Field(default=None)
    syncedlyrics: str = Field(default=None)
    isrc: str = Field(default=None)


class Config(BaseSettings):
    APPNAME: str = 'mixel-music'
    VERSION: str = '0.7.0'
    HOST: str = '0.0.0.0'
    PORT: int = 2843

    DATADIR: Path = get_path('data')
    LOGPATH: Path = get_path(DATADIR, 'mixel-music.log')
    ARTWORKDIR: Path = get_path(DATADIR, 'artworks')
    LIBRARYDIR: Path = get_path('library')

    ARTWORKFORMAT: str = 'webp'
    ARTWORKCACHING: bool = True
    ARTWORKQUALITY: int = 100
    ARTWORKTARGETS: set = {'.png', '.jpg', '.jpeg', '.tiff'}

    DEBUG: bool = True
    DBECHO: bool = False
    LOGLEVEL: int = logging.DEBUG
    DBURL: str = "sqlite+aiosqlite:///" \
        + str_path(DATADIR, 'database.db', rel=False)
    
Config = Config()