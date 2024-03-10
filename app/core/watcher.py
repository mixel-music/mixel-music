from watchfiles import Change, awatch
from core.library import *
from core.models import *
from infra.session import *
from tools.standard_path import *
import asyncio

path_property = {}

async def find_changes():
    """
    It retrieves all track information from the database and checks if the files actually exist with matching sizes.

    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """
    async with session() as conn:
        track_info = await conn.execute(select(Tracks.path, Tracks.size))
        track_info = track_info.fetchall()

    if track_info:
        async with asyncio.TaskGroup() as tg:
            for path_data, size_data in track_info:
                real_path = get_path(path_data)
                if not real_path.exists():
                    tg.create_task(Library.remove(path_data))
                elif real_path.stat().st_size != size_data:
                    tg.create_task(Library.remove(path_data))
                else:
                    path_property[path_data] = 'skip'
    await library_scan()

async def library_scan(path: Path = library_dir()):
    queue = [path]
    while queue:
        current_path = queue.pop(0)
        for path in current_path.iterdir():
            if path.is_dir():
                path_property[str_path(path)] = 'dir'
                queue.append(path)
            else:
                if path_property.get(str_path(path)) == 'skip':
                    path_property.pop(str_path(path), None)
                elif is_music_file(str_path(path)):
                    asyncio.create_task(Library.create(str_path(path)))

async def watch_change():
    logs.info("Event watcher initiated.")
    async for event_handler in awatch(library_dir(), recursive=True, force_polling=True):
        async with asyncio.TaskGroup() as tg:
            for event_type, event_path in event_handler:
                strpath = str_path(event_path)
                if is_music_file(strpath):
                    if event_type == Change.added:
                        tg.create_task(Library.create(strpath))
                    elif event_type == Change.deleted:
                        tg.create_task(Library.remove(strpath))
                    elif event_type == Change.modified:
                        tg.create_task(Library.update(strpath))