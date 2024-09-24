from concurrent.futures import ThreadPoolExecutor
import asyncio

from models import *
from core.database import *
from core.logging import *
from tools.path_handler import *
from tools.tags_handler import *
from repos.library import *

semaphore = asyncio.Semaphore(5)

class LibraryTask:
    def __init__(self, path: str) -> None:
        self.path = path
        self.tags = {}


    async def create_track(self) -> None:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            self.tags = await loop.run_in_executor(executor, extract_tags, self.path)

        if self.tags:
            async with semaphore:
                async with db_conn() as conn:
                    repo = LibraryRepo(conn)
                    await repo.insert_track(self.tags)
                    logs.debug(f"Track inserted: {self.tags.get('title')}")


    async def remove_track(self) -> None:
        async with semaphore:
            async with db_conn() as conn:
                repo = LibraryRepo(conn)
                await repo.delete_track(self.path)
                logs.debug(f"Track removed: {self.path}")
