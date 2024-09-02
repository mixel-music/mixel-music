from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):

    DB_URL: str = "sqlite+aiosqlite:///" \
        + str_path('config', 'mixel-music.db', rel=False)




    TITLE: str = 'mixel-music'
    VERSION: str = '0.5.1'
    HOST: str = '0.0.0.0'
    PORT: int = 2843

    I18N_DIR: Path = get_path('i18n')
    DATA_DIR: Path = get_path('config')
    LOG_PATH: Path = get_path('config', '.log')
    MUSIC_DIR: Path = get_path('library')

    IMG_DIR: Path = get_path('config', 'artworks')
    IMG_TYPE: str = 'webp'
    IMG_QUAL: int = 100

    LOG_LEVEL: int = logging.DEBUG
    DB_ECHO: bool = True
    DEBUG: bool = True

conf = Config()