from watchfiles import Change, DefaultFilter, awatch
from tools import *
from .music import *

logging.basicConfig(
    filename=PathTools.abs_path('conf', '.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def filter(path, change_type):
    allowed_extensions = ['.mp3', '.mp4', '.wav', '.flac']
    return path.suffix in allowed_extensions

async def scan():
    target_path = PathTools.abs_path('library')
    logging.debug("Starting...")
    
    async for changes in awatch(target_path, watch_filter=filter):
        print(changes)

        # if event.is_directory:
        #     return None
        # elif event.event_type == 'created':
        #     file = Tracks(PathTools.get_path(event.src_path))