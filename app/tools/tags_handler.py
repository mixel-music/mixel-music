from tinytag import TinyTag
from datetime import datetime
import re

from core.logging import *
from models.track import TrackItem
from tools.path_handler import *
from tools.convert_value import hash_str, get_mime, safe_list

artist_patterns = {
    'bracket': re.compile(r'\s*\([^)]*[:;,][^)]*\)'),
    'details': re.compile(r'\s*feat\.?\s.*'),
    'year_month_day': re.compile(r'^(\d{4})[-., ]?(\d{1,2})[-., ]?(\d{1,2})$'),  # YYYY-MM-DD, YYYY.MM.DD, YYYYMMDD, etc.
    'year_month': re.compile(r'^(\d{4})[-., ]?(\d{1,2})$'),                      # YYYY-MM, YYYY.MM, YYYYMM, etc.
    'year': re.compile(r'^(\d{4})$')                                             # YYYY only
}

def convert_date(date_input) -> tuple[str, int]:
    try:
        if isinstance(date_input, int):
            date_input = str(date_input)
    
        match = artist_patterns['year_month_day'].match(date_input)
        if match:
            year, month, day = match.groups()
            month = month.zfill(2)
            day = day.zfill(2)

            return f"{year}-{month}-{day}", year

        match = artist_patterns['year_month'].match(date_input)
        if match:
            year, month = match.groups()
            month = month.zfill(2)

            return f"{year}-{month}", year

        match = artist_patterns['year'].match(date_input)
        if match:
            year = match.group(1)
            return year, year
    except:
        return '', 0


def convert_artist(data: str) -> str:
    try:
        artist_value = artist_patterns['bracket'].sub('', data)
        artist_value = artist_patterns['details'].sub('', data)

        return artist_value
    
    except:
        return ''


def extract_tags(path: str) -> TrackItem:
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
