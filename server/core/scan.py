from watchfiles import Change, awatch
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
        tracks.select().with_only_columns([tracks.c.path, tracks.c.hash])
    )

    if tracks_list:
        for tracks_info in tracks_list:
            tracks_real_path = get_path(tracks_info['path'], rel=False)
            if not tracks_real_path.exists():
                await delete(tracks_info['path'])
            else:
                async with aiofiles.open(tracks_real_path, mode='rb') as afile:
                    tracks_hash = hashlib.md5(await afile.read()).hexdigest().upper()
                if tracks_info['hash'] != tracks_hash:
                    await delete(tracks_info['path'])
                else:
                    file_states[tracks_info['path']] = 'skip'

    asyncio.create_task(scan_path())

async def scan_path(path: Path = LIBRARY_PATH):
    tasks = []
    for target in path.iterdir():
        if file_states.get(get_strpath(target)) == 'skip':
            continue
        elif target.is_file() and target.suffix in SUFFIXES:
            task = asyncio.create_task(insert(target))
            tasks.append(task)
        elif target.is_dir():
            file_states[get_strpath(target)] = 'dir'
            try:
                task = asyncio.create_task(scan_path(target))
                tasks.append(task)
            except FileNotFoundError:
                logs.error("File not found. unexcepted behavior.")

    await asyncio.gather(*tasks)

async def scan_auto():
    logs.info("Library observer initiated.")

    async for events in awatch(LIBRARY_PATH, recursive=True):
       for events_type, events_path in events:
            events_path = Path(events_path)

            if events_type == Change.added or events_type == Change.modified:
                if events_path.is_dir():
                    file_states[get_strpath(events_path)] = 'dir'
                    await scan_path(events_path)
                else:
                    if events_path.suffix in SUFFIXES:
                        if events_type is Change.modified: await delete(events_path)
                        asyncio.create_task(insert(events_path))
            elif events_type == Change.deleted:
                if file_states.get(get_strpath(events_path)) == 'dir':
                    asyncio.create_task(delete(events_path))
                else:
                    if events_path.suffix in SUFFIXES:
                        asyncio.create_task(delete(events_path))

async def insert(path):
    async with sem:
        try:
            tracks_obj = Tracks(get_strpath(path))
            await tracks_obj.insert()
        except:
            print("Failed to insert data into the database.")

async def delete(path):
    tracks_obj = Tracks(get_strpath(path))
    await tracks_obj.delete(file_states.get(get_strpath(path)))

    file_states.pop(path, None)