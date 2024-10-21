import os
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from tools.path_handler import get_path, str_path, Path

load_dotenv()

class ConfigData(BaseSettings):
    HOST: str = str(os.getenv('HOST'))
    PORT: int = int(os.getenv('PORT'))
    DATADIR: Path = get_path('data')
    LOGPATH: Path = get_path(DATADIR, 'mixel-music.log')
    ARTWORKDIR: Path = get_path(DATADIR, 'artworks')
    LIBRARYDIR: Path = get_path('library')
    ARTWORKFORMAT: str = 'webp'
    ARTWORKCACHING: bool = os.getenv('ARTWORKCACHING').lower() in ['true', '1', 'yes']
    ARTWORKQUALITY: int = int(os.getenv('ARTWORKQUALITY'))
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
    
Config = ConfigData()
