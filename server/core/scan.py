from watchfiles import Change, DefaultFilter, awatch
from mutagen import File, MutagenError
from core.images import *
from core.tracks import *
from tools.path import *
from core.logs import *

LIBRARY_PATH = get_path('library', rel=False)
sem = asyncio.Semaphore(8)
file_states = {}

async def init_scan():
    tracks_list = await db.fetch_all(
        tracks.select().with_only_columns([tracks.c.path, tracks.c.size])
    )
    if tracks_list:
        async with asyncio.TaskGroup() as scan:
            for tracks_info in tracks_list:
                tracks_real_path = get_path(tracks_info['path'], rel=False)
                if not tracks_real_path.exists():
                    scan.create_task(delete(tracks_info['path']))
                else:
                    tracks_size = tracks_real_path.stat().st_size
                    if tracks_info['size'] != tracks_size:
                        scan.create_task(delete(tracks_info['path']))
                    else:
                        file_states[tracks_info['path']] = 'skip' 
    await scan_path()

async def scan_path(path: Path = LIBRARY_PATH):
    async with asyncio.TaskGroup() as scan:
        for target in path.iterdir():
            if file_states.get(get_strpath(target)) == 'skip':
                file_states.pop(get_strpath(target), None)
                continue
            elif target.is_file() and target.suffix in SUFFIXES:
                await insert(target)
                image_task = Images(target)
                asyncio.create_task(image_task.image_extract())
            elif target.is_dir():
                file_states[get_strpath(target)] = 'dir'
                scan.create_task(scan_path(target))

class ScanFilter(DefaultFilter):
    def __call__(self, change: Change, path: str) -> bool:
        pure_path = PurePath(path)
        suffix = pure_path.suffix
        diff_path = get_strpath(pure_path.parent)
        library_path = get_strpath(LIBRARY_PATH)

        if suffix == '' or (diff_path == library_path and suffix in SUFFIXES):
            return (super().__call__(change, path) and path)

async def scan_auto():
    logs.info("Library observer initiated.")
    async for events in awatch(
        LIBRARY_PATH,
        recursive=True,
        watch_filter=ScanFilter(),
        debug=True,
    ):
       for events_type, events_path in events:
            events_path = Path(events_path)

            if events_type == Change.added or events_type == Change.modified:
                if events_path.is_dir():
                    file_states[get_strpath(events_path)] = 'dir'
                    asyncio.create_task(scan_path(events_path))
                else:
                    if events_type == Change.modified: await delete(events_path)
                    await insert(events_path)
                    image_task = Images(events_path)
                    asyncio.create_task(image_task.image_extract())
            elif events_type == Change.deleted:
                if file_states.get(get_strpath(events_path)) == 'dir':
                    asyncio.create_task(delete(events_path))
                else:
                    asyncio.create_task(delete(events_path))

async def insert(path):
    async with sem:
        try:
            tracks_obj = Tracks(get_strpath(path))
            await tracks_obj.insert()
        except:
            logs.error("Failed to insert data into the database.")

async def delete(path):
    tracks_obj = Tracks(get_strpath(path))
    await tracks_obj.delete(file_states.get(get_strpath(path)))
    file_states.pop(get_strpath(path), None)