from watchfiles import Change, awatch
import asyncio

from core.config import Config
from core.database import *
from core.logging import *
from services.library_scan import *
from services.library_task import *
from tools.path_handler import *


async def scanner() -> None:
    """
    It retrieves all track information from the database and checks if the files actually exist with matching sizes.

    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """

    path_props, tasks = {}, []
    
    async with db_conn() as conn:
        repo = LibraryRepo(conn)
        track_info = await repo.get_scan_info()

    if track_info:
        for path_data, size_data in track_info:
            real_path = get_path(path_data)

            if not real_path.exists() or real_path.stat().st_size != size_data:
                tasks.append(LibraryTask(path_data).remove_track())
            else:
                path_props[path_data] = 'p' # 'PASS'

        await asyncio.gather(*tasks)

    await library_scanner(props=path_props)
    asyncio.create_task(LibraryScan.perform_all())


async def library_scanner(props: dict, path = None) -> None:
    if path is None: path = Config.LIBRARYDIR
    queue, tasks = [path], []

    while queue:
        current_path = queue.pop(0)
        for path in current_path.iterdir():
            path_value = str_path(path)

            if path.is_dir():
                props[path_value] = 'd' # 'DIR'
                queue.append(path)

            elif is_supported_file(path_value):
                if props.get(path_value) == 'p':
                    props.pop(path_value, None)
                else:
                    tasks.append(LibraryTask(path_value).create_track())

    await asyncio.gather(*tasks)


async def tracker() -> None:
    logs.info("Started scanning for library.")

    async for event_handler in awatch(
        Config.LIBRARYDIR,
        recursive=True,
        force_polling=True,
    ):
        tasks = []
        
        for event_type, event_path in event_handler:
            str_path_val = str_path(event_path)

            if is_supported_file(str_path_val):
                instance = LibraryTask(str_path_val)

                if event_type == Change.added:
                    tasks.append(instance.create_track())
                elif event_type == Change.deleted:
                    tasks.append(instance.remove_track())
                # elif event_type == Change.modified:
                #     tasks.append(instance.update_track()) TODO

        await asyncio.gather(*tasks)
        asyncio.create_task(LibraryScan.perform_all())
