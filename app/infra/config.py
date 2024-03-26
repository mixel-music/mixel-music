from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///" \
        + str_path('mixel-music.db', rel=False)
    TITLE: str = 'mixel-music'
    DEBUG: bool = True
    LOG_LEVEL: int = logging.DEBUG
    HOST: str = '127.0.0.1'
    PORT: int = 2843
    VERSION: str = '0.2.6a'
    SQL_ECHO: bool = True
    IMG_QUAL: int = 100
    IMG_TYPE: str = 'webp'
    IMG_SIZE: list[int] = [128, 300, 500]

    DATA_DIR: Path = get_path('task')
    CONFIG_DIR: Path = get_path('task')
    IMAGES_DIR: Path = get_path('task', 'images')
    LIBRARY_DIR: Path = get_path('music')

    LOG_PATH: Path = get_path('mixel-music.txt')
    TASK_DIR: Path = get_path('task')
    IMAGE_DIR: Path = get_path('task', 'image')
    MUSIC_DIR: Path = get_path('music')

conf = Config()