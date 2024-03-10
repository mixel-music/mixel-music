from core.models import Tracks
from infra.session import *
import hashlib

def list_join(value: list) -> str:
    return ', '.join(str(v) for v in value) if isinstance(value, list) else str(value)

def get_hash_str(*args) -> str:
    try:
        return hashlib.md5(''.join(str(arg) for arg in args).encode()).hexdigest().upper()
    except ValueError:
        return ''

def sanitize_num(num: int) -> int:
    if isinstance(num, tuple): num = num[0]
    try: return int(num)
    except ValueError: return 0

async def hash_to_image(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.imagehash).where(Tracks.hash == hash)
            )
            row = result.scalars().first()
    except:
        return ''

    return row if row else ''
    
async def hash_to_track(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.path).where(Tracks.hash == hash)
            )
            row = result.scalars().first()
    except:
        return ''
        
    return row if row else ''