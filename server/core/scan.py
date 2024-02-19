from watchfiles import Change, awatch
from mutagen import File, MutagenError
from core.images import *
from core.tracks import *
from tools.path import *
from core.logs import *

LIBRARY_PATH = get_path('library', rel=False)
sem = asyncio.Semaphore(8)
file_states = {}

async def scan_path(path: Path = LIBRARY_PATH):
    tasks = []
    for target in path.iterdir():
        if target.is_file():
            file_states[target] = 'file'
            task = asyncio.create_task(upcert(target))
            tasks.append(task)

        elif target.is_dir():
            file_states[target] = 'dir'
            task = asyncio.create_task(scan_path(target))
            tasks.append(task)

        await asyncio.gather(*tasks)

async def scan_auto():
    logs.info("Library observer initiated.")

    async for events in awatch(LIBRARY_PATH, recursive=True):
        for events_type, events_path in events:
            events_path = Path(events_path)

            if events_type == Change.added or events_type == Change.modified:
                if events_path.is_dir():
                    file_states[events_path] = 'dir'
                else:
                    file_states[events_path] = 'file'
                    asyncio.create_task(upcert(events_path))
            elif events_type == Change.deleted:
                asyncio.create_task(delete(events_path))

async def upcert(path: Path):
    async with sem:
        try:
            is_track = File(path)
            if path.suffix and is_track:
                file_id = get_hash(get_strpath(path))
                file_id_list = await db.fetch_one(
                    tracks.select().with_only_columns([tracks.c.id]).where(tracks.c.id == file_id)
                )

                if file_id_list:
                    return False
                else:
                    tracks_obj = Tracks(get_strpath(path))
                    image_task = Images(path)
                    asyncio.create_task(tracks_obj.upcert(), name=f"event_{path}")
                    asyncio.create_task(image_task.image_extract_db())
        except (MutagenError, IOError):
            return False

async def delete(path: Path):
    tracks_obj = Tracks(get_strpath(path))
    await tracks_obj.delete(file_states.get(path))

    file_states.pop(path, None)