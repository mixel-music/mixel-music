import hashlib
import mimetypes

from models import *
from core.logger import *
from core.database import *
from tools.path_handler import *

def get_mime(path: str) -> list[str]:
    try:
        type = mimetypes.guess_type(get_path(path), strict=True)
        if type:
            return type[0]
        else:
            return 'application/octet-stream'
    except:
        return 'application/octet-stream'


def hash_str(*args) -> str:
    try:
        return hashlib.md5(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''


async def hash_track_to_album(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.album_id).where(Tracks.track_id == hash)
            )
            row = result.scalars().first()
        
        return row if row else ''

    except Exception as error:
        logs.error("Failed to get albumhash, %s", error)
        return ''
    
    
async def hash_track_to_path(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.filepath).where(Tracks.track_id == hash)
            )
            row = result.scalars().first()

        return row if row else ''
    
    except Exception as error:
        logs.error("Failed to get track's path, %s", error)
        return ''
    

def safe_list(extra, key, default=''):
    extra = dict(extra)
    try:
        value = extra.get(key, [default])
        return value[0] if value else default
    except:
        return ''