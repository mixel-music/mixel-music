from watchfiles import Change, awatch
from sqlalchemy import select
import asyncio

from core.library import *
from core.models import Tracks
from infra.database import *
from infra.loggings import *
from tools.path_handler import *

async def find_changes() -> None:
    """
    It retrieves all track information from the database and checks if the files actually exist with matching sizes.
    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """

    path_property, tasks = {}, []
    
    async with session() as conn:
        track_info = await conn.execute(select(Tracks.path, Tracks.size))
        track_info = track_info.all()

    if track_info:
        for path_data, size_data in track_info:
            real_path = get_path(path_data)

            if not real_path.exists() or real_path.stat().st_size != size_data:
                tasks.append(LibraryTask(path_data).remove_track())
            else:
                path_property[path_data] = 'p' # Pass

        await asyncio.gather(*tasks)

    await library_scan(property = path_property)
    await LibraryTask.perform_albums()


async def library_scan(property: dict, path = None) -> None:
    if path is None: path = conf.MUSIC_DIR
    queue, tasks = [path], []

    while queue:
        current_path = queue.pop(0)
        for path in current_path.iterdir():
            str_path_val = str_path(path)

            if path.is_dir():
                property[str_path_val] = 'd' # Dir
                queue.append(path)

            elif is_music_file(str_path_val):
                if property.get(str_path_val) == 'p':
                    property.pop(str_path_val, None)
                else:
                    tasks.append(LibraryTask(str_path_val).create_track())

    await asyncio.gather(*tasks)


async def watch_change() -> None:
    logs.info("Event watcher initiated.")
    tasks = []

    async for event_handler in awatch(
        conf.MUSIC_DIR,
        recursive=True,
        force_polling=True,
    ):

        for event_type, event_path in event_handler:
            str_path_val = str_path(event_path)

            if is_music_file(str_path_val):
                instance = LibraryTask(str_path_val)

                if event_type == Change.added:
                    tasks.append(instance.create_track())
                elif event_type == Change.deleted:
                    tasks.append(instance.remove_track())
                # elif event_type == Change.modified:
                #     tasks.append(instance.update_track()) TODO

        await asyncio.gather(*tasks)