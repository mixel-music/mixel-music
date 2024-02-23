from watchfiles import Change, awatch
from core.images import *
from core.tracks import *
from tools.path import *
from core.logs import *

LIBRARY_PATH = get_path('library', rel=False)
sem = asyncio.Semaphore(8)

file_states = {}
'''It use get_strpath(*args) as the key.'''

async def check_db_data():
    """
    It first retrieves all track information from the database and checks if the files actually exist with matching sizes.

    If a file doesn't exist or the size differs, it is removed from the database; otherwise, it is excluded from the library scan.
    """
    tracks_list = await db.fetch_all(
        tracks.select().with_only_columns([tracks.c.path, tracks.c.size])
    )
    if tracks_list:
        async with asyncio.TaskGroup() as scan:
            for path_data, size_data in tracks_list:
                real_path = get_path(path_data, rel=False)

                if not real_path.exists():
                    scan.create_task(event_delete(path_data))
                else:
                    tracks_size = real_path.stat().st_size
                    if size_data != tracks_size:
                        scan.create_task(event_delete(path_data))
                    else:
                        file_states[path_data] = 'skip'
    await scan_dir_path()

async def scan_dir_path(path: Path = LIBRARY_PATH):
    """
    It retrieves all directories and files from the selected path, checks the suffix, and creates a track object if the path leads to a file.
    
    If the path is a directory, it adds "the path is a directory" to file_states, and recursively calls itself to scan the subdirectories.
    """
    async with asyncio.TaskGroup() as scan:
        for scan_path in path.iterdir():
            strpath = get_strpath(scan_path)
            suffix = get_name(strpath)[2]

            if file_states.get(strpath) == 'skip':
                file_states.pop(strpath, None)
            elif suffix in SUFFIXES:
                scan.create_task(event_create(strpath))
            elif scan_path.is_dir():
                file_states[strpath] = 'dir'
                scan.create_task(scan_dir_path(scan_path))

async def event_watcher():
    """
    It only detects directory creation and deletion to prevent unexcepted behavior.

    If a directory is created or deleted, it starts the directory scanning task.
    """
    logs.info("Event watcher initiated.")
    async for event_handler in awatch(LIBRARY_PATH, recursive=True, force_polling=True):
        for event_type, event_path in event_handler:
            path = get_path(event_path)
            strpath = get_strpath(event_path)
            suffix = get_name(strpath)[2]

            if suffix == '' or file_states.get(strpath) == 'dir':
                print(strpath)
                if event_type == Change.added:
                    await event_create(strpath, 'dir')
                if event_type == Change.deleted:
                    await event_delete(strpath, 'dir')
            elif suffix in SUFFIXES:
                if event_type in [Change.added or Change.modified]:
                    await event_create(strpath)
                elif event_type == Change.deleted and path.parent.exists():
                    await event_delete(strpath)

async def event_create(path: str, path_type: str = None):
    tracks_obj = Tracks(path)
    if path_type == 'dir':
        file_states[path] = 'dir'
        print("It's directory.")
    else:
        async with sem:
            await tracks_obj.insert()

async def event_delete(path: str, path_type: str = None):
    tracks_obj = Tracks(path)
    if path_type == 'dir': file_states.pop(path, None)
    await tracks_obj.delete(path_type)