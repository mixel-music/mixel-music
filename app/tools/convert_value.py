import hashlib
import mimetypes
from core.models import *
from infra.database import *
from infra.loggings import *
from tools.path_handler import *

def guess_mime(path: str) -> list[str]:
    try:
        type = mimetypes.guess_type(get_path(path), strict=True)
        if type:
            return type[0]
        else:
            return 'application/octet-stream'
    except:
        return 'application/octet-stream'

def get_hash_str(*args) -> str:
    try:
        return hashlib.sha1(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''

def sanitize_num(num: int) -> int:
    if isinstance(num, tuple): num = num[0]
    try:
        return int(num)
    except ValueError:
        return 0
    
def sanitize_float(str: str) -> float:
    try:
        return float(str)
    except ValueError:
        return 0.0

async def hash_to_albumhash(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.albumhash).where(Tracks.hash == hash)
            )
            row = result.scalars().first()
    except Exception as err:
        logs.error("Failed to get image path from hash, %s", err)
        return ''

    return row if row else ''
    
async def hash_to_track(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.path).where(Tracks.hash == hash)
            )
            row = result.scalars().first()
    except Exception as err:
        logs.error("Failed to get track path from hash, %s", err)
        return ''
        
    return row if row else ''