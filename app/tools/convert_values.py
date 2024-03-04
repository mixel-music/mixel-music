from core.models import Tracks
from infra.session import *
import hashlib

def list_join(value: list) -> str:
    return ', '.join(str(v) for v in value) if isinstance(value, list) else str(value)

def get_hash_str(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest().upper()

def sanitize_num(num: int) -> int:
    if isinstance(num, tuple): num = num[0]
    try: return int(num)
    except ValueError: return 0

async def hash_to_image(hash: str) -> str:
    query = await db.fetch_one(
        select(Tracks.imagehash).where(Tracks.hash == hash)
    )
    return query.imagehash if query and query.imagehash else None
    
async def hash_to_track(hash: str) -> str:
    query = await db.fetch_one(
        select(Tracks.path).where(Tracks.hash == hash)
    )
    return query.path if query else None