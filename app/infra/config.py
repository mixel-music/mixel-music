from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///" + str_path('data', 'database.db', rel=False)
    TITLE: str = 'mixel-music'
    DEBUG: bool = True
    LOG_LEVEL: int = logging.DEBUG
    SQL_LEVEL: int = logging.WARN
    HOST: str = '127.0.0.1'
    PORT: int = 2843
    VERSION: str = '0.2.3a'
    SQL_ECHO: bool = True
    IMG_QUAL: int = 100
    IMG_TYPE: str = 'webp'
    IMG_SIZE: list[int] = [128, 300, 500]
    DATA_DIR: Path = get_path('data')
    IMAGES_DIR: Path = get_path('data', 'images')
    LIBRARY_DIR: Path = get_path('library')
    LOG_PATH: Path = get_path('data', '.log')

conf = Config()