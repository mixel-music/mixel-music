from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    TITLE: str = 'mixel-music'
    HOST: str = '127.0.0.1'
    PORT: int = 2843

    DB_URL: str = "sqlite+aiosqlite:///" \
        + str_path('config', 'database.db', rel=False)
    I18N_DIR: Path = get_path('i18n')
    DATA_DIR: Path = get_path('config')
    LOG_PATH: Path = get_path('config', '.log')
    MUSIC_DIR: Path = get_path('assets')

    IMG_DIR: Path = get_path('config', 'images')
    IMG_SIZE: list[int] = [128, 300, 500]
    IMG_TYPE: str = 'webp'
    IMG_QUAL: int = 100

    DEBUG: bool = True
    DB_ECHO: bool = False
    VERSION: str = '0.3.0'
    LOG_LEVEL: int = logging.DEBUG

conf = Config()