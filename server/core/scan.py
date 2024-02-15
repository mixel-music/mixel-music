from watchfiles import Change, awatch
from tools import *
from .music import *

logging.basicConfig(
    filename=PathTools.abs_path('conf', '.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

suffix = ['.mp3', '.flac', '.wav', '.m4a', '.mp4', '.alac', '.opus'] # test

async def scan():
    target_path = PathTools.abs_path('library')
    logging.debug("Starting...")
    
    async for changes in awatch(target_path):
        for change_type, path in changes:
            file_path = Path(path)
            if file_path.suffix in suffix:
                if change_type == Change.added:
                    await handle_file_creation(file_path)
                elif change_type == Change.deleted:
                    await handle_file_deletion(file_path)

async def handle_file_creation(file_path):
    file = Tracks(PathTools.get_path(file_path))
    await file.find_track()

async def handle_file_deletion(file_path):
    file = Tracks(PathTools.get_path(file_path))
    await file.find_track()
    await file.delete_track()