from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///" + str_path('config', 'database.db', rel=False)
    APP_TITLE: str = 'mixel-music'
    LOG_LEVEL: int = logging.DEBUG
    SQLALCHEMY_LEVEL: int = logging.WARN
    FASTAPI_DEBUG: bool = True
    APP_HOST: str = '127.0.0.1'
    APP_PORT: int = 2843
    VERSION: str = '0.2.2a'
    SQL_ECHO: bool = True
    IMG_QUAL: int = 100
    IMG_TYPES: str = 'webp'
    IMG_SIZES: list[int] = [128, 300, 500]
    CONFIG_DIR: Path = get_path('config')
    IMAGES_DIR: Path = get_path('config', 'images')
    LIBRARY_DIR: Path = get_path('library')
    LOG_FILE_PATH: Path = get_path('config', '.log')

conf = Config()