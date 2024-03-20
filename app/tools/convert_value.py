import hashlib
from core.models import *
from infra.database import *
from infra.loggings import *
from tools.path_handler import *

def list_join(value: list) -> str:
    return ', '.join(str(v) for v in value) if isinstance(value, list) else str(value)

def get_hash_str(*args) -> str:
    try:
        return hashlib.sha1(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''

# TODO: use pydantic
def sanitize_num(num: int) -> int:
    if isinstance(num, tuple): num = num[0]
    try:
        return int(num)
    except ValueError:
        return 0

def album_values(old: dict, tags: dict) -> dict:
    return {
        'tracktotals': max(tags.get('tracktotals'), old.get('tracktotals')),
        'durationtotals': old.get('durationtotals') + tags.get('duration'),
        'sizetotals': old.get('sizetotals') + tags.get('size', 0),
        'imagehash': tags.get('imagehash') if not old.get('imagehash') else old.get('imagehash'),
        'musicbrainz_albumartistid': tags.get('musicbrainz_albumartistid') if not old.get('musicbrainz_albumartistid') else old.get('musicbrainz_albumartistid'),
        'musicbrainz_albumid': tags.get('musicbrainz_albumid') if not old.get('musicbrainz_albumid') else old.get('musicbrainz_albumid'),
    }

async def hash_to_image(hash: str) -> str:
    try:
        async with session() as conn:
            result = await conn.execute(
                select(Tracks.imagehash).where(Tracks.hash == hash)
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