from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from rich.progress import track
from infra.config import *
import logging
import time

def init_logger():
    install(word_wrap=True)
    console = Console(record=True, soft_wrap=True)

    base_rich_handler = RichHandler(console=console, rich_tracebacks=True)
    base_rich_handler.setLevel(logging.INFO)

    debug_rich_handler = RichHandler(console=console, rich_tracebacks=True)
    debug_rich_handler.setLevel(conf.LOG_LEVEL)

    root_logger = logging.getLogger()
    root_logger.setLevel(conf.LOG_LEVEL)
    root_logger.addHandler(base_rich_handler)

    for logger_name in [conf.TITLE, "uvicorn", "fastapi"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(conf.LOG_LEVEL)

        logger.addHandler(debug_rich_handler)
        logger.propagate = False

    return console

logs = logging.getLogger(conf.TITLE)