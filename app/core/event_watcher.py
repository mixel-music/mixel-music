from watchfiles import Change, awatch
from core.library_handler import *
from core.tracks_service import *
from infra.path_handler import *
from infra.setup_logger import *

path_property = {}

async def check_changes():
    """
    It retrieves all track information from the database and checks if the files actually exist with matching sizes.

    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """
    track_info = await db.fetch_all(
        tracks.select().with_only_columns([tracks.c.path, tracks.c.size])
    )
    if track_info:
        async with asyncio.TaskGroup() as tg:
            for path_data, size_data in track_info:
                real_path = get_path(path_data)
                if not real_path.exists():
                    tg.create_task(LibraryHandler.remove(path_data))
                elif real_path.stat().st_size != size_data:
                    tg.create_task(LibraryHandler.remove(path_data))
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
                    asyncio.create_task(LibraryHandler.create(str_path(path)))

async def event_watcher():
    logs.info("Event watcher initiated.")
    async for event_handler in awatch(library_dir(), recursive=True, force_polling=True):
        async with asyncio.TaskGroup() as tg:
            for event_type, event_path in event_handler:
                strpath = str_path(event_path)
                if is_music_file(strpath):
                    if event_type == Change.added:
                        tg.create_task(LibraryHandler.create(strpath))
                    elif event_type == Change.deleted:
                        await LibraryHandler.remove(strpath)