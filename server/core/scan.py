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
        db_tracks = await db.fetch_all(tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]))
        for db_tracks_path in db_tracks:
            if not get_path(db_tracks_path['path'], is_rel=False, is_str=False).exists():
                logs.info("Removing untracked file...")
                await db.execute(tracks.delete().where(tracks.c.path == db_tracks_path['path']))
            if not get_path('data', 'images', db_tracks_path['imageid'], is_rel=False, is_str=False).exists():
                logs.info("Removing untracked image...")
                for img_path_delete in get_path('data', 'images', is_rel=False, is_str=False).glob(f"{db_tracks_path['imageid']}*"):
                    if img_path_delete.is_file():
                        img_path_delete.unlink(missing_ok=True)

        # Listing and checking MIME types of all files
        dir_tracks = list(target_real_path.glob('**/*'))

        tasks = [ScanTools.create(dir_tracks_path) for dir_tracks_path in dir_tracks]
        await asyncio.gather(*tasks)

        logs.info("Complete manual scanning.")
        return None

    @staticmethod
    async def scan_detect():
        logs.info("Library observer initiated.")

        async for events in awatch(target_real_path, recursive=True):
            for events_type, events_path in events:
                events_path = get_path(events_path, is_rel=False, is_str=False)

                if events_path.is_dir and events_type == Change.deleted:
                    await ScanTools.delete_dir(events_path)
                    continue # Preventing deletion if the target directory contains files

                if events_type == Change.modified:
                    await ScanTools.modify(events_path)
                    continue # Storing original file's creation data before modifications
                elif events_type == Change.added:
                    await ScanTools.create(events_path)
                elif events_type == Change.deleted:
                    await ScanTools.delete(events_path)

    @staticmethod
    async def create(path: Path):
        if get_mime(get_path(path, is_rel=False)) is True:
            logs.debug("Initiating insert process...")
            tracks_obj = TracksObject(get_path(path))
            await tracks_obj.insert()

            logs.debug("Initiating create image id...")
            images_obj = ImagesObject(get_path(path))
            await images_obj.image_extract_db()

    @staticmethod
    async def modify(path: Path):
        if get_mime(get_path(path, is_rel=False)) is True:
            logs.debug("Initiating modify process...")
            tracks_obj = TracksObject(get_path(path))
            await tracks_obj.update()

            logs.debug("Initiating update image id...")
            images_obj = ImagesObject(get_path(path))
            await images_obj.image_extract_db()

    @staticmethod
    async def delete(path: Path):
        if get_mime(get_path(path, is_rel=False)) is True:
            logs.debug("Initiating delete process...")
            tracks_obj = TracksObject(get_path(path))
            await tracks_obj.delete()

    @staticmethod
    async def delete_dir(path: Path):
        dir_path = get_path(path)
        logs.debug("Initiating delete process...")

        img_path = await db.fetch_one(tracks.select().with_only_columns([tracks.c.imageid]).where(tracks.c.path.like(f'{dir_path}%')))

        # Removing all images from database with names starting from the image id
        if img_path:
            img_path_target = img_path['imageid']
            img_path = get_path('data', 'images', is_rel=False, is_str=False)
        else:
            return None
        
        for img_path_delete in img_path.glob(f"{img_path_target}*"):
            if img_path_delete.is_file():
                img_path_delete.unlink(missing_ok=True)

        # Removing all tracks from database with paths starting from the target directory
        await db.execute(tracks.delete().where(tracks.c.path.like(f'{dir_path}%')))