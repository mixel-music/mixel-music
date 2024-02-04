from fastapi import APIRouter
from server.utils.modules import *
import mutagen
from mutagen import MutagenError, mp3, m4a, mp4, flac, wave, oggopus, aac

router = APIRouter()

@router.get("/tracks")
async def api_tracks():
    ext_enable = (".mp3", ".m4a", ".flac", ".alac", ".wav", ".opus", ".aac")
    music_path = os.path.join(get_root_path(), "test")
    music_files = []

    for root, dirs, files in os.walk(music_path):
        for filename in files:
            if any(filename.endswith(extension) for extension in ext_enable):
                name, ext = os.path.splitext(filename)
                relpath = os.path.relpath(os.path.join(root, filename), music_path)
                music_files.append([name, relpath])

    return music_files