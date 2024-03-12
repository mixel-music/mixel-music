from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from tools.standard_path import *
import logging

install()

print_console = Console(
    record=True,
    soft_wrap=True
)
print_handler = RichHandler(
    console=print_console,
    rich_tracebacks=True
)
write_console = Console(
    file=open(log_path(), "a", encoding='utf-8'),
    record=True,
)
write_handler = RichHandler(
    console=write_console,
    rich_tracebacks=True
)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
fastapi_logger = logging.getLogger("fastapi")
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
logs = logging.getLogger('mixel-music')

uvicorn_logger.setLevel(logging.DEBUG)
uvicorn_access_logger.setLevel(logging.DEBUG)
fastapi_logger.setLevel(logging.DEBUG)
sqlalchemy_logger.setLevel(logging.WARN)
logs.setLevel(logging.DEBUG)

uvicorn_logger.propagate = False
uvicorn_access_logger.propagate = False
fastapi_logger.propagate = False
sqlalchemy_logger.propagate = False
logs.propagate = False

def logging() -> None:
    uvicorn_logger.addHandler(print_handler)
    uvicorn_access_logger.addHandler(print_handler)
    fastapi_logger.addHandler(print_handler)
    sqlalchemy_logger.addHandler(print_handler)
    logs.addHandler(print_handler)
    logs.addHandler(write_handler)

def stop_logging() -> None:
    uvicorn_logger.removeHandler(print_handler)
    uvicorn_access_logger.removeHandler(print_handler)
    fastapi_logger.removeHandler(print_handler)
    sqlalchemy_logger.removeHandler(print_handler)
    logs.removeHandler(print_handler)
    logs.removeHandler(write_handler)