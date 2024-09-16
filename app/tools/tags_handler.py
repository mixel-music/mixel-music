from tinytag import TinyTag
from datetime import datetime
import re

from core.logger import *
from tools.path_handler import *
from tools.convert_value import hash_str, get_mime

g_pattern = re.compile(r'\s*\([^)]*[:;,][^)]*\)')
f_pattern = re.compile(r'\s*feat\.?\s.*')

def convert_artist(data: str) -> str:
    try:
        artist_value = g_pattern.sub('', data)
        artist_value = f_pattern.sub('', data)

        return artist_value
    
    except:
        return ''


def extract_tags(path: str) -> dict:
    path, real_path = str_path(path), get_path(path)
    
    try:
        tags = TinyTag.get(real_path)
        if tags.extra.get('unsyncedlyrics', ''):
            if not tags.extra.get('syncedlyrics', '') or tags.extra.get('lyrics', ''):
                lyrics = tags.extra_get('unsyncedlyrics', '')
            elif tags.extra.get('syncedlyrics', ''):
                lyrics = tags.extra_get('syncedlyrics', '')
            elif tags.extra.get('lyrics', ''):
                lyrics = tags.extra_get('lyrics', '')
        else:
            lyrics = ''

        track_dict = {
            'track_id': hash_str(path),
            'album_id': tags.album or '',
            'artist_id': hash_str(convert_artist(tags.artist)) if tags.artist else '',
            'albumartist_id': hash_str(tags.albumartist) if tags.albumartist else '',
            'title': tags.title or get_filename(path)[0],
            'album': tags.album or '',
            'albumartist': tags.albumartist or '',
            'composer': tags.composer or '',
            'artist': tags.artist or '',
            'genre': tags.genre or '',
            'total_track': tags.track_total or 0,
            'total_disc': tags.disc_total or 0,
            'track': tags.track or 0,
            'disc': tags.disc or 0,
            'isrc':
                tags.extra.get('isrc', '')[0] if tags.extra.get('isrc', '') else '',
            'label': 
                tags.extra.get('label', '')[0] if tags.extra.get('label', '') else '',
            'lyrics': lyrics,
            'comment': tags.comment or '',
            'copyright':
                tags.extra.get('copyright', '')[0] if tags.extra.get('copyright', '') else '',
            'filepath': path,
            'filesize': tags.filesize or 0,
            'duration': tags.duration or 0,
            'mime': get_mime(path),
            'date': tags.year or 0,
            'year': tags.year or 0,
            'bitrate': tags.bitrate or 0.0,
            'bitdepth': tags.bitdepth or 0,
            'channels': tags.channels or 0,
            'samplerate': tags.samplerate or 0,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }

        return track_dict
    
    except Exception as error:
        logs.error('Failed to extract, %s', error)
        return {}


def extract_artwork(path: str) -> bytes | None:
    try:
        artwork = TinyTag.get(get_path(path), image=True)
        return artwork.get_image() if artwork else None
    except:
        return None