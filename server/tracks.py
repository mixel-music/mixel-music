from fastapi import APIRouter
from pathlib import Path
from server.utils.modules import *

router = APIRouter()

@router.get("/tracks")
async def api_tracks():
    ext_enable = [".mp3", ".m4a", ".flac", ".alac", ".wav", ".opus", ".aac"]
    music_dir = Path(get_root_path(), "test")
    music_files = [file.name for file in music_dir.iterdir() if file.suffix in ext_enable]
    return {"music_files": music_files}