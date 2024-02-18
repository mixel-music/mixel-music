from watchfiles import Change, awatch
from model.model import *
from core.images import *
from core.tracks import *
from tools.path import *
from tools.tags import *
from core.logs import *

target_real_path = get_path('library', is_rel=False, is_str=False)
target_path = get_path(target_real_path)

class ScanTools:
    @staticmethod
    async def scan_manual():
        logs.info("Starting manual scan...")

        # Checking untracked files before scanning
        db_tracks = await db.fetch_all(tracks.select().with_only_columns([tracks.c.path]))
        for db_tracks_path in db_tracks:
            if not get_path(db_tracks_path['path'], is_rel=False, is_str=False).exists():
                logs.info("Removing untracked files...")
                await db.execute(tracks.delete().where(tracks.c.path == db_tracks_path['path']))

        # Listing and checking MIME types of all files
        dir_tracks = list(target_real_path.glob('**/*'))

        for dir_tracks_path in dir_tracks:
            if not get_mime(dir_tracks_path) is None:
                await ScanTools.create(dir_tracks_path)

        logs.info("Complete manual scanning.")
        return None

    @staticmethod
    async def scan_detect():
        logs.info("Library observer initiated.")

        async for events in awatch(target_real_path, recursive=True):
            for events_type, events_path in events:
                events_path = get_path(events_path, is_rel=False, is_str=False)

                if events_path.is_dir() and events_type == Change.deleted:
                    await ScanTools.delete_dir(events_path)
                    continue # Preventing deletion if the target directory contains files

                if not get_mime(events_path) is None:
                    if events_type == Change.modified:
                        await ScanTools.modify(events_path)
                        continue # Storing original file's creation data before modifications
                    elif events_type == Change.added:
                        await ScanTools.create(events_path)
                    elif events_type == Change.deleted:
                        await ScanTools.delete(events_path)

    @staticmethod
    async def create(path: Path):
        logs.debug("Initiating insert process...")
        tracks_obj = Tracks(get_path(path))
        await tracks_obj.insert()

    @staticmethod
    async def modify(path: Path):
        logs.debug("Initiating modify process...")
        tracks_obj = Tracks(get_path(path))
        await tracks_obj.update()

    @staticmethod
    async def delete(path: Path):
        logs.debug("Initiating delete process...")
        tracks_obj = Tracks(get_path(path))
        await tracks_obj.delete()

    @staticmethod
    async def delete_dir(path: Path):
        dir_path = get_path(path)

        img_path = await db.fetch_one(
            tracks.select().with_only_columns[tracks.c.imageid]
        ).where(
            Tracks.c.path.like(f'{dir_path}%')
        )

        # Removing all images from database with names starting from the image id
        if img_path:
            img_path_target = img_path['image_id']
            img_path = get_path('data', 'images', is_rel=False, is_str=False)
        else:
            return None
        
        for img_path_delete in img_path.glob(f"{img_path_target}*"):
            if img_path_delete.is_file():
                img_path_delete.unlink(missing_ok=True)

        # Removing all tracks from database with paths starting from the target directory
        await db.execute(tracks.delete().where(tracks.c.path.like(f'{dir_path}%')))