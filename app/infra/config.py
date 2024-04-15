from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    TITLE: str = 'mixel-music'
    HOST: str = '127.0.0.1'
    PORT: int = 2843

    DB_URL: str = "sqlite+aiosqlite:///" \
        + str_path('data', 'database.db', rel=False)
    I18N_DIR: Path = get_path('i18n')
    DATA_DIR: Path = get_path('data')
    LOG_PATH: Path = get_path('data', '.log')
    MUSIC_DIR: Path = get_path('music')

    IMG_DIR: Path = get_path('data', 'images')
    IMG_SIZE: list[int] = [128, 300, 500]
    IMG_TYPE: str = 'webp'
    IMG_QUAL: int = 100

    DEBUG: bool = True
    DB_ECHO: bool = False
    VERSION: str = '0.2.9a'
    LOG_LEVEL: int = logging.DEBUG

conf = Config()