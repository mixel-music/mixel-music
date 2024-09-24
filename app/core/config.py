from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    APPNAME: str = 'mixel-music'
    VERSION: str = '0.11.0'
    HOST: str = '0.0.0.0'
    PORT: int = 2843
    DATADIR: Path = get_path('data')
    LOGPATH: Path = get_path(DATADIR, 'mixel-music.log')
    ARTWORKDIR: Path = get_path(DATADIR, 'artworks')
    LIBRARYDIR: Path = get_path('library')
    ARTWORKFORMAT: str = 'webp'
    ARTWORKCACHING: bool = True
    ARTWORKQUALITY: int = 100
    ARTWORKTARGETS: set = {
        '.png',
        '.jpg',
        '.jpeg',
        '.tiff'
    }
    DEBUG: bool = True
    DBECHO: bool = False
    LOGLEVEL: int = logging.DEBUG
    DBURL: str = "sqlite+aiosqlite:///" \
        + str_path(DATADIR, 'database.db', rel=False)
    
Config = Config()
