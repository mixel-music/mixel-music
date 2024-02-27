from watchfiles import Change, awatch
from core.tracks_service import *
from infra.init_logger import *
from infra.handle_path import *

LIBRARY_PATH = get_path('library')
sem = asyncio.Semaphore(8)
path_property = {}

async def check_changes():
    """
    It first retrieves all track information from the database and checks if the files actually exist with matching sizes.

    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """
    tracks_list = await db.fetch_all(
        tracks.select().with_only_columns([tracks.c.imageid, tracks.c.path, tracks.c.size])
    )
    if tracks_list:
        async with asyncio.TaskGroup() as scan:
            for image_id, path_data, size_data in tracks_list:
                real_path = get_path(path_data)

                if not real_path.exists():
                    scan.create_task(event_remove(path_data))
                    image_path = get_path('data', 'images')
                    for image_file in image_path.glob(f"{image_id}*"):
                        if image_file.exists(): image_file.unlink(missing_ok=True)
                else:
                    tracks_size = real_path.stat().st_size
                    if size_data != tracks_size:
                        scan.create_task(event_remove(path_data))
                    else:
                        path_property[path_data] = 'skip'
    await library_scan()

async def library_scan(path: Path = LIBRARY_PATH):
    """
    It retrieves all directories and files from the selected path, checks the suffix, and creates a track if the path leads to a file.
    
    If the path is a directory, it adds a property to the file for skipping, and recursively calls itself to scan the subdirectories.
    """
    async with asyncio.TaskGroup() as scan:
        for scan_path in path.iterdir():
            strpath = str_path(scan_path)
            suffix = get_filename(strpath)[2]

            if path_property.get(strpath) == 'skip':
                path_property.pop(strpath, None)
            elif suffix in SUFFIXES:
                scan.create_task(event_create(strpath))
            elif scan_path.is_dir():
                path_property[strpath] = 'dir'
                scan.create_task(library_scan(scan_path))

async def event_watcher():
    logs.info("Event watcher initiated.")
    async for event_handler in awatch(LIBRARY_PATH, recursive=True, force_polling=True):
        for event_type, event_path in event_handler:
            strpath = str_path(event_path)
            suffix = get_filename(strpath)[2]

            if suffix in SUFFIXES:
                if event_type == Change.added:
                    asyncio.create_task(event_create(strpath))
                elif event_type == Change.deleted:
                    asyncio.create_task(event_remove(strpath))

async def event_create(path: str):
    async with sem:
        tracks = TracksService(path)
        await tracks.create()

async def event_remove(path: str):
    tracks = TracksService(path)
    await tracks.remove()