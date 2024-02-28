from watchfiles import Change, awatch
from core.library_handler import *
from core.tracks_service import *
from infra.path_handler import *
from infra.setup_logger import *

sem = asyncio.Semaphore(8)
path_property = {}

async def check_changes():
    """
    It first retrieves all track information from the database and checks if the files actually exist with matching sizes.

    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """
    track_info = await db.fetch_all(
        tracks.select().with_only_columns([tracks.c.path, tracks.c.size])
    )

    if track_info:
        for path_data, size_data in track_info:
            real_path = get_path(path_data)
            if not real_path.exists():
                asyncio.create_task(LibraryHandler.remove(path_data))
            else:
                tracks_size = real_path.stat().st_size
                if size_data != tracks_size:
                    asyncio.create_task(LibraryHandler.remove(path_data))
                else:
                    path_property[path_data] = 'skip'

    await library_scan()

async def library_scan(path: Path = library_dir()):
    """
    It retrieves all directories and files from the selected path, checks the suffix, and creates a track if the path leads to a file.
    
    If the path is a directory, it adds a property for skipping, and recursively calls itself to scan the subdirectories.
    """
    async with asyncio.TaskGroup() as scan:
        for scan_path in path.iterdir():
            strpath = str_path(scan_path)
            if path_property.get(strpath) == 'skip':
                path_property.pop(strpath, None)
            elif scan_path.is_dir():
                path_property[strpath] = 'dir'
                scan.create_task(library_scan(scan_path))
            elif is_music_file(strpath):
                logs.debug("Event detected during post scanning!")
                scan.create_task(LibraryHandler.create(strpath))

async def event_watcher():
    logs.info("Event watcher initiated.")
    async for event_handler in awatch(library_dir(), recursive=True, force_polling=True):
        for event_type, event_path in event_handler:
            strpath = str_path(event_path)

            if is_music_file(strpath):
                if event_type == Change.added:
                    asyncio.create_task(LibraryHandler.create(strpath))
                elif event_type == Change.deleted:
                    asyncio.create_task(LibraryHandler.remove(strpath))