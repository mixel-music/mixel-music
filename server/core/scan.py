from watchfiles import Change, awatch
from core.images import *
from core.tracks import *
from tools.path import *
from core.logs import *

LIBRARY_PATH = get_path('library', rel=False)
sem = asyncio.Semaphore(8)
path_property = {}

async def check_db_data():
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
                real_path = get_path(path_data, rel=False)

                if not real_path.exists():
                    scan.create_task(event_delete(path_data))
                    image_path = get_path('data', 'images', rel=False)
                    for image_file in image_path.glob(f"{image_id}*"):
                        if image_file.exists(): image_file.unlink(missing_ok=True)
                else:
                    tracks_size = real_path.stat().st_size
                    if size_data != tracks_size:
                        scan.create_task(event_delete(path_data))
                    else:
                        path_property[path_data] = 'skip'
    await scan_dir_path()

async def scan_dir_path(path: Path = LIBRARY_PATH):
    """
    It retrieves all directories and files from the selected path, checks the suffix, and creates a track object if the path leads to a file.
    
    If the path is a directory, it adds "the path is a directory" to path_property, and recursively calls itself to scan the subdirectories.
    """
    async with asyncio.TaskGroup() as scan:
        for scan_path in path.iterdir():
            strpath = get_strpath(scan_path)
            suffix = get_name(strpath)[2]

            if path_property.get(strpath) == 'skip':
                path_property.pop(strpath, None)
            elif suffix in SUFFIXES:
                scan.create_task(event_create(strpath))
            elif scan_path.is_dir():
                path_property[strpath] = 'dir'
                scan.create_task(scan_dir_path(scan_path))

async def event_watcher():
    logs.info("Event watcher initiated.")
    async for event_handler in awatch(LIBRARY_PATH, recursive=True, force_polling=True):
        for event_type, event_path in event_handler:
            strpath = get_strpath(event_path)
            suffix = get_name(strpath)[2]

            if suffix in SUFFIXES:
                if event_type == Change.added:
                    asyncio.create_task(event_create(strpath))
                elif event_type == Change.deleted:
                    asyncio.create_task(event_delete(strpath))

async def event_create(path: str):
    async with sem:
        tracks_obj = Tracks(path)
        await tracks_obj.insert()
        
        images_obj = Images(path)
        await images_obj.extract()

async def event_delete(path: str):
    tracks_obj = Tracks(path)
    await tracks_obj.delete()