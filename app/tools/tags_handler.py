from tinytag import TinyTag
from datetime import datetime
import re
from types import SimpleNamespace

from core.logger import *
from tools.path_handler import *
from tools.convert_value import hash_str, get_mime, safe_list

g_pattern = re.compile(r'\s*\([^)]*[:;,][^)]*\)')
f_pattern = re.compile(r'\s*feat\.?\s.*')

patterns = {
    'full_date': re.compile(r'^(\d{4})[-., ]?(\d{1,2})[-., ]?(\d{1,2})$'),  # YYYY-MM-DD, YYYY.MM.DD, YYYYMMDD, etc.
    'year_month': re.compile(r'^(\d{4})[-., ]?(\d{1,2})$'),                 # YYYY-MM, YYYY.MM, YYYYMM, etc.
    'year_only': re.compile(r'^(\d{4})$')                                   # YYYY only
}

def convert_date(date_input):
    try:
        if isinstance(date_input, int):
            date_input = str(date_input)
    
        match = patterns['full_date'].match(date_input)
        if match:
            year, month, day = match.groups()
            month = month.zfill(2)
            day = day.zfill(2)

            return f"{year}-{month}-{day}", year

        match = patterns['year_month'].match(date_input)
        if match:
            year, month = match.groups()
            month = month.zfill(2)

            return f"{year}-{month}", year

        match = patterns['year_only'].match(date_input)
        if match:
            year = match.group(1)
            return year, year
    except:
        return '', 0


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

        date, year = convert_date(tags.year)
        if tags.album:
            album_id = hash_str(
                tags.album,
                tags.albumartist or '',
                tags.track_total or 0,
                str_path(get_path(path).parent),
            )
        else:
            album_id = hash_str(
                tags.artist,
                tags.albumartist or '',
                str_path(get_path(path).parent),
            )
        
        if tags.albumartist:
            albumartist_id = hash_str(tags.albumartist.lower())
        elif tags.artist:
            albumartist_id = hash_str(tags.artist.lower())


        track_dict = {
            'album': tags.album or '',
            'album_id': album_id,
            'albumartist': tags.albumartist or '',
            'albumartist_id': albumartist_id,
            'artist': tags.artist or '',
            'artist_id': hash_str(convert_artist(tags.artist.lower())) or '',
            'artwork_id': '',
            'bitdepth': tags.bitdepth or 0,
            'bitrate': tags.bitrate or 0.0,
            'channels': tags.channels or 0,
            'comment': tags.comment or '',
            'compilation': True if safe_list(tags.extra, 'compilation') else False,
            'composer': tags.composer or '',
            'content_type': get_mime(path),
            'created_at': datetime.now(),
            'date': date,
            'director': safe_list(tags.extra, 'director'),
            'directory': str_path(get_path(path).parent),
            'duration': tags.duration or 0.0,
            'disc_number': tags.disc or 0,
            'disc_total': tags.disc_total or 0,
            'filepath': path,
            'filesize': tags.filesize or 0,
            'genre': tags.genre or '',
            'isrc': safe_list(tags.extra, 'isrc'),
            'label': safe_list(tags.extra, 'label'),
            'lyrics': '',
            'samplerate': tags.samplerate or 0,
            'title': tags.title or '',
            'track_id': hash_str(path),
            'track_number': tags.track or 0,
            'track_total': tags.track_total or 0,
            'updated_at': datetime.now(),
            'year': year,

            # 'hash': hash_str(path),
            # 'title': tags.title or get_filename(path)[0] or 'Unknown Title',
            # 'artisthash': hash_str(convert_artist(tags.artist)),
            # 'albumhash': '',
            # 'albumartisthash': hash_str(tags.albumartist) or '',
            # 'disc': tags.disc or 0,
            # 'disctotal': tags.disc_total or 0,
            # 'size': tags.filesize or 0,
            # 'track': tags.track or 0,
            # 'tracktotal': tags.track_total or 0,
            # 'directory': str_path(get_path(path).parent, rel=True),
            # 'mime': get_mime(path),
            # 'path': path,
            # 'created_date': datetime.now(),
            # 'updated_date': datetime.now(),
            # 'unsyncedlyrics': '',
            # 'syncedlyrics': '',
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