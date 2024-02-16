from watchfiles import Change, awatch
from tools import *
from .music import *

class ScanTools:
    @staticmethod
    async def scan():
        tarconvert = PathTools.abs('library')
        logging.debug("Starting...")

        async for changes in awatch(tarconvert, recursive=True):
            for change_type, path in changes:
                file_path = Path(path)

                if change_type == Change.deleted and not file_path.suffix:
                    await ScanTools.delete_dir(file_path)
                    continue

                if PathTools.is_music(file_path):
                    if change_type == Change.added:
                        await ScanTools.create_file(file_path)
                    elif change_type == Change.deleted:
                        await ScanTools.delete_file(file_path)

    @staticmethod
    async def create_file(file_path: Path):
        music = Tracks(PathTools.std(file_path))
        await music.lookup()

    @staticmethod
    async def delete_file(file_path: Path):
        music = Tracks(PathTools.std(file_path))
        await music.delete()

    @staticmethod
    async def delete_dir(dir_path: Path):
        diff_path = PathTools.std(dir_path)
        query = music.delete().where(music.c.path.like(f'{diff_path}%'))
        await database.execute(query)