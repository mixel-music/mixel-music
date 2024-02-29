from infra.database import *
import hashlib

def list_join(value: list) -> str:
    return ', '.join(str(v) for v in value) if isinstance(value, list) else str(value)

def get_hash_str(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest().upper()

def sanitize_num(num: int) -> int:
    if isinstance(num, tuple): num = num[0]
    try: return int(num)
    except ValueError: return 0

async def id_to_image_id(id: str) -> str:
    db_result = await db.fetch_one(tracks.select().with_only_columns([tracks.c.imageid]).where(tracks.c.trackid == id))
    image_id = db_result.imageid if db_result and db_result.imageid else None
    
    return image_id
    
async def id_to_str_path(id: str) -> str:
    query = await db.fetch_one(
        tracks.select().with_only_columns(tracks.c.path).where(tracks.c.trackid == id)
    )
    return query.path if query else None