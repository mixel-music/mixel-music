from pathlib import Path
import aiosqlite

global valid_ext
valid_ext = (".mp3", ".m4a", ".flac", ".alac", ".wav", ".opus", ".aac")

async def db_conn():
    path_data = get_abs_path('data')
    
    db = await aiosqlite.connect(Path(path_data / 'database.db'))

def get_abs_path(*args) -> Path:
    """
    Returns an absolute path, defaults to the project's root.
    """
    abs_path = Path(__file__).parents[2]
    
    if args is None:
        return abs_path
    
    for arg in args:
        abs_path = abs_path / arg

    return abs_path


def check_ext_valid(path: str) -> bool:
    """
    Check if the path is a media file.
    """
    file = Path(path)
    ext = file.suffix

    if ".." in path or ext.lower() not in valid_ext: return False
    if not file.is_file(): return False

    return True