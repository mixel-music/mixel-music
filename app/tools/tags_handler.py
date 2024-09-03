from tinytag import TinyTag
from datetime import datetime

from core.logger import *
from tools.path_handler import *
from tools.convert_value import hash_str, get_mime

async def extract_tags(path: str) -> dict:
    path, real_path = str_path(path), get_path(path)
    
    try:
        tags = TinyTag.get(real_path)
        track_dict = {
            'hash': hash_str(path),
            'title': tags.title or get_filename(path)[0] or 'Unknown Title',
            'artist': tags.artist or 'Unknown Artist',
            'artisthash': hash_str(tags.artist) if tags.artist else '',
            'album': tags.album or 'Unknown Album',
            'albumhash': '',
            'albumartist': tags.albumartist or '',
            'bitdepth': tags.bitdepth or 0,
            'bitrate': tags.bitrate or 0.0,
            'channels': tags.channels or 0,
            'comment': tags.comment or '',
            'composer': tags.composer or '',
            'disc': tags.disc or 0,
            'disctotal': tags.disc_total or 0,
            'duration': tags.duration or 0.0,
            'size': tags.filesize or 0,
            'genre': tags.genre or '',
            'samplerate': tags.samplerate or 0,
            'track': tags.track or 0,
            'tracktotal': tags.track_total or 0,
            'year': tags.year or 'Unknown Year',
            'directory': get_filename(path)[1],
            'mime': get_mime(path),
            'path': path,
            'created_date': datetime.now(),
            'updated_date': datetime.now(),
            'isrc': tags.extra.get('isrc', '')[0] if tags.extra.get('isrc', '') else '',
            'unsyncedlyrics': '',
            'syncedlyrics': '',
        }
        return track_dict
    
    except Exception as error:
        logs.error('Failed to extract, %s', error)
        return {}


async def extract_artwork(path: str) -> bytes | None:
    try:
        artwork = TinyTag.get(get_path(path), image=True)
        return artwork.get_image() if artwork else None
    except:
        return None