from watchfiles import Change, DefaultFilter, awatch
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
                    scan.create_task(delete(path_data))
                else:
                    tracks_size = real_path.stat().st_size
                    if size_data != tracks_size:
                        scan.create_task(delete(path_data))
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

            if file_states.get(strpath) == 'skip':
                file_states.pop(strpath, None)
                continue
            elif scan_path.is_file() and scan_path.suffix in SUFFIXES:
                await insert(scan_path)
                image_task = Images(scan_path)
                asyncio.create_task(image_task.extract())
                # insert, 이미지 처리 로직 개선 필요
            elif scan_path.is_dir():
                file_states[strpath] = 'dir'
                scan.create_task(scan_dir_path(scan_path))

class EventFilter(DefaultFilter):
    def __call__(self, change: Change, path: str) -> bool:
        pure_path = PurePath(path)
        diff_path = get_strpath(pure_path.parent)
        library_path = get_strpath(LIBRARY_PATH)
        suffix = pure_path.suffix

        if suffix == '' or (diff_path == library_path and suffix in SUFFIXES):
            return (super().__call__(change, path) and path)

async def event_watcher():
    """
    It only detects directory creation and deletion to prevent unexcepted behavior.

    If a directory is created or deleted, it starts the directory scanning task.
    """
    logs.info("Event watcher initiated.")
    async for events in awatch(
        LIBRARY_PATH,
        recursive=True,
        watch_filter=EventFilter(),
    ):
       for events_type, events_path in events:
            events_path = Path(events_path)

            if events_type == Change.added or events_type == Change.modified:
                if events_path.is_dir():
                    file_states[get_strpath(events_path)] = 'dir'
                    asyncio.create_task(scan_dir_path(events_path))
                else:
                    if events_type == Change.modified: await delete(events_path)
                    await insert(events_path)
                    image_task = Images(events_path)
                    asyncio.create_task(image_task.extract())
                    # insert, 이미지 처리 로직 개선 필요
            elif events_type == Change.deleted:
                if file_states.get(get_strpath(events_path)) == 'dir':
                    asyncio.create_task(delete(events_path))
                else:
                    asyncio.create_task(delete(events_path))

async def insert(path):
    async with sem:
        tracks_obj = Tracks(get_strpath(path))
        await tracks_obj.insert()

async def delete(path):
    tracks_obj = Tracks(get_strpath(path))
    await tracks_obj.delete(file_states.get(get_strpath(path)))
    file_states.pop(get_strpath(path), None)