from fastapi import APIRouter, Response, HTTPException, Header
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC, Picture
from mutagen import File
from pathlib import *

global valid_ext
valid_ext = (".mp3", ".m4a", ".flac", ".alac", ".wav", ".opus", ".aac")

def get_abs_path(dir_1st: str = None, dir_2nd: str = None) -> Path:
    """
    Return the project's root directory as an absolute path.
    """
    if dir_1st is None:
        return Path(__file__).parents[2]
    elif dir_1st is not None and dir_2nd is None:
        return Path(__file__).parents[2] / dir_1st
    else:
        return Path(__file__).parents[2] / dir_1st / dir_2nd

def check_ext_valid(path: str) -> bool:
    """
    Check if the path is a media file.
    """
    file = Path(path)
    ext = file.suffix

    if ".." in path or ext.lower() not in valid_ext: return False
    if not file.is_file(): return False

async def get_music_info(path: str) -> tuple:
    """
    Identify the type of media file and extract its metadata.
    """
    ext = Path(path).suffix
    mp_image = []

    if ext == '.mp3':
        mp = ID3(path)

        mp_title = mp.get('TIT2', 'Unknown Title')[0]
        mp_artist = mp.get('TPE1', 'Unknown Artist')[0]
        mp_album = mp.get('TALB', 'Unknown Album')[0]
        mp_year = mp.get('TDRC', 'Unknown Year')[0]

        for tag in mp.values():
            if isinstance(tag, APIC):
                mp_image = tag.data # Set first image to front cover
                break

    elif ext == '.flac':
        mp = FLAC(path)

        mp_title = mp.get('title', ['Unknown Title'])[0]
        mp_artist = mp.get('artist', ['Unknown Artist'])[0]
        mp_album = mp.get('album', ['Unknown Album'])[0]
        mp_year = mp.get('date', ['Unknown Year'])[0]

        if mp.pictures:
            mp_image = mp.pictures[0].data # Set first image to front cover

    else:
        return False

    mp_image = mp_image if mp_image else False

    return mp_title, mp_artist, mp_album, mp_year, mp_image