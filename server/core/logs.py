from tools.path import *
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
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
    file=open(get_path('data', 'tamaya.log', is_rel=False), "a"),
    record=True,
)

write_handler = RichHandler(
    console=write_console,
    rich_tracebacks=True
)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.DEBUG)
uvicorn_logger.propagate = False
uvicorn_logger.addHandler(print_handler)
uvicorn_logger.addHandler(write_handler)

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.setLevel(logging.DEBUG)
uvicorn_access_logger.propagate = False
uvicorn_access_logger.addHandler(print_handler)
uvicorn_access_logger.addHandler(write_handler)

fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.setLevel(logging.DEBUG)
fastapi_logger.addHandler(print_handler)
fastapi_logger.addHandler(write_handler)

logs = logging.getLogger('tamaya')
logs.propagate = False
logs.setLevel(logging.DEBUG)
logs.addHandler(print_handler)
logs.addHandler(write_handler)

logs.debug("Initializing logger...")