from concurrent.futures import ThreadPoolExecutor
import asyncio

from models import *
from core.database import *
from core.logging import *
from tools.path_handler import *
from tools.tags_handler import *
from repos.library import *

semaphore = asyncio.Semaphore(5) # 이거 안 하면 락걸림

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
                async with session() as conn:
                    try:
                        logs.debug("Inserting \"%s\"", self.tags.get('title'))
                        await LibraryRepo(conn).insert_track(self.tags)
                        await conn.commit()

                    except Exception as error:
                        logs.error("Failed to create. %s", error)
                        await conn.rollback()


    async def remove_track(self) -> None:
        async with semaphore:
            async with session() as conn:
                try:
                    logs.debug("Removing \"%s\"", self.path)
                    await LibraryRepo(conn).delete_track(self.path)
                    await conn.commit()

                except Exception as error:
                    logs.error("Failed to remove. %s", error)
                    await conn.rollback()