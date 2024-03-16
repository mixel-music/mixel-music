from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from infra.config import *
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
write_console = Console(
    file = open(
        conf.LOG_FILE_PATH,
        "a",
        encoding='utf-8'
    ),
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
logs = logging.getLogger(conf.APP_TITLE)

uvicorn_logger.setLevel(conf.LOG_LEVEL)
uvicorn_access_logger.setLevel(conf.LOG_LEVEL)
fastapi_logger.setLevel(conf.LOG_LEVEL)
sqlalchemy_logger.setLevel(conf.SQLALCHEMY_LEVEL)
logs.setLevel(conf.LOG_LEVEL)

uvicorn_logger.propagate = False
uvicorn_access_logger.propagate = False
fastapi_logger.propagate = False
sqlalchemy_logger.propagate = False
logs.propagate = False

uvicorn_logger.addHandler(print_handler)
uvicorn_access_logger.addHandler(print_handler)
fastapi_logger.addHandler(print_handler)
sqlalchemy_logger.addHandler(print_handler)
logs.addHandler(print_handler)
logs.addHandler(write_handler)