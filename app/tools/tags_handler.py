from datetime import datetime
from tinytag import TinyTag
from typing import Any
from tools.path_handler import get_path, str_path
from tools.convert_value import (
    hash_str,
    get_mime,
    safe_list,
    convert_date,
    convert_artist,
)


def extract_tags(path: str) -> dict[str, Any]:
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
    
    except:
        return {}


def extract_artwork(path: str) -> bytes | None:
    try:
        artwork = TinyTag.get(get_path(path), image=True)
        return artwork.get_image() if artwork else None
    except:
        return None
