from infra.database import *
from infra.handle_path import *
from infra.init_logger import *
import hashlib

SUFFIXES = [
    '.3gp',
    '.aif',
    '.aifc',
    '.aiff',
    '.amr',
    '.avi',
    '.flac',
    '.m4a',
    '.m4b',
    '.m4p',
    '.m4r',
    '.m4v',
    '.mkv',
    '.mov',
    '.mp3',
    '.mp4',
    '.mpg',
    '.ogg',
    '.wav',
    '.webm',
    '.wmv',
]

def get_hash_str(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest().upper()

def sanitize_num(value: int) -> int:
    try:
        return int(value)
    except ValueError:
        return 0
    
async def id_to_str_path(id: str) -> str:
    query = await db.fetch_one(
        tracks.select().with_only_columns(tracks.c.path).where(tracks.c.id == id)
    )
    return query.path if query else None
    
async def check_suffix(path: str | Path) -> bool:
    suffix = Path(path).suffix
    return True if suffix == [check for check in SUFFIXES] else False