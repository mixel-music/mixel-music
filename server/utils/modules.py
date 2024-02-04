from fastapi import APIRouter, Response, HTTPException, Header
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC, Picture
from mutagen import File
import os

global valid_ext
valid_ext = (".mp3", ".MP3", ".m4a", ".M4A", ".flac", ".FLAC", ".alac", ".ALAC", ".wav", ".WAV", ".opus", ".OPUS", ".aac", "AAC")

async def get_root_path():
    """
    Return root directory path of the project to access another folder
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def get_split_path(full_path: str) -> tuple:
    """
    Split filename and extension from full path.
    """
    str_name, str_ext = os.path.splitext(full_path)
    return str_name, str_ext

async def check_ext_valid(file_path: str) -> bool:
    """
    check the extension of a given file path to identify the file type
    """
    ext = (await get_split_path(file_path))[1]
    
    if ext not in valid_ext or ".." in file_path: return False
    if not os.path.isfile(file_path): return False

async def music_metadata(music_path: str) -> tuple:
    """
    Check the file extension and export metadata using mutagen
    """
    ext = (await get_split_path(music_path))[1]
    mp_image = []

    if ext == '.mp3':
        mp = ID3(music_path)

        mp_title = mp.get('TIT2', 'Unknown Title')[0]
        mp_artist = mp.get('TPE1', 'Unknown Artist')[0]
        mp_album = mp.get('TALB', 'Unknown Album')[0]
        mp_year = mp.get('TDRC', 'Unknown Year')[0]

        for tag in mp.values():
            if isinstance(tag, APIC):
                mp_image = tag.data # Set first image to front cover
                break

    elif ext == '.flac':
        mp = FLAC(music_path)

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