from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from core.config import Config
import logging

install(word_wrap=True)

print_console = Console(
    record=True,
    soft_wrap=True,
)

print_handler = RichHandler(
    console=print_console,
    rich_tracebacks=True
)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
fastapi_logger = logging.getLogger("fastapi")
logs = logging.getLogger(Config.APPNAME)

uvicorn_logger.setLevel(Config.LOGLEVEL)
uvicorn_access_logger.setLevel(Config.LOGLEVEL)
fastapi_logger.setLevel(Config.LOGLEVEL)
logs.setLevel(Config.LOGLEVEL)

uvicorn_logger.propagate = False
uvicorn_access_logger.propagate = False
fastapi_logger.propagate = False
logs.propagate = False

uvicorn_logger.addHandler(print_handler)
uvicorn_access_logger.addHandler(print_handler)
fastapi_logger.addHandler(print_handler)
logs.addHandler(print_handler)

def log_file_handler() -> logging.FileHandler:
    file_handler = logging.FileHandler(
        Config.LOGPATH,
        mode='a',
        encoding='utf-8'
    )

    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logs.addHandler(file_handler)
    
    return file_handler
