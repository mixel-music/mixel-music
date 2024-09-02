from pydantic_settings import BaseSettings
from tools.path_handler import *
import logging

class Config(BaseSettings):
    AppName: str = 'mixel-music'
    Version: str = '0.5.2'
    Host: str = '0.0.0.0'
    Port: int = 2843

    ConfigDir: Path = get_path('config')
    LibraryDir: Path = get_path('library')
    ArtworkDir: Path = get_path('config', 'artworks')
    LogFileDir: Path = get_path('config', '.log')

    ArtworkFormat: str = 'webp'
    ArtworkQuality: int = 100
    ArtworkPreload: bool = True

    LogLevel: int = logging.DEBUG
    Debug: bool = True

    DataBaseEcho: bool = False
    DataBaseUrl: str = "sqlite+aiosqlite:///" \
        + str_path('config', 'mixel-music.db', rel=False)

conf = Config()