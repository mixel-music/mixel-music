from watchfiles import Change, awatch
from tools import *
from .music import *

target_path = PathTools.abs('library')

class ScanTools:
    @staticmethod
    async def manual_scan():
        logging.debug("Manual scan activated. Scanning...")
        target_file = []

        for suffix in allow_suffix:
            target_file += list(target_path.glob(f'**/*{suffix}'))

        if not target_file:
            query = music.delete()
            await database.execute(query=query)

            return None
        
        for target in target_file:
            music_class = Tracks(PathTools.std(target))
            await music_class.lookup()

        return None

    @staticmethod
    async def change_scan():
        logging.debug("Starting...")

        async for changes in awatch(target_path, recursive=True):
            for change_type, path in changes:
                file_path = Path(path)

                if change_type == Change.deleted and not file_path.suffix:
                    await ScanTools.delete_dir(file_path)
                    continue

                if PathTools.is_music(file_path):
                    if change_type == Change.modified:
                        await ScanTools.modify_file(file_path)
                        continue
                    elif change_type == Change.added:
                        await ScanTools.create_file(file_path)
                    elif change_type == Change.deleted:
                        await ScanTools.delete_file(file_path)

    @staticmethod
    async def create_file(file_path: Path):
        music = Tracks(PathTools.std(file_path))
        await music.lookup()

    @staticmethod
    async def modify_file(file_path: Path):
        music = Tracks(PathTools.std(file_path))
        await music.update()

    @staticmethod
    async def delete_file(file_path: Path):
        music = Tracks(PathTools.std(file_path))
        await music.delete()

    @staticmethod
    async def delete_dir(dir_path: Path):
        diff_path = PathTools.std(dir_path)
        query = music.delete().where(music.c.path.like(f'{diff_path}%'))
        await database.execute(query)