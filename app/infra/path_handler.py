from pathlib import Path
import filetype

SUFFIXES = [
    '.3gp',
    '.aif',
    '.aifc',
    '.aiff',
    '.amr',
    '.avi',
    '.flac',
    '.m4a',
    '.m4b',
    '.m4p',
    '.m4r',
    '.m4v',
    '.mkv',
    '.mov',
    '.mp3',
    '.mp4',
    '.mpg',
    '.ogg',
    '.wav',
    '.webm',
    '.wmv',
]

root = (Path.cwd().resolve()).parent

def get_path(*args: str | Path, rel: bool = False) -> Path:
    """
    Abstracts a path-like object or string path within the application and returns it as a path-like object.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to False.
    """
    home = root
    for arg in args: home = home / arg
    if rel: home = home.relative_to(root)

    return home

def str_path(*args: str | Path, rel: bool = True) -> str:
    """
    Abstracts a path-like object or string path within the application and returns it as a string.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to True.
    """
    home = root
    for arg in args: home = home / arg
    if rel: home = home.relative_to(root)

    return home.as_posix()

def config_dir() -> Path:
    return get_path('config')

def images_dir() -> Path:
    return get_path('config', 'images')

def library_dir() -> Path:
    return get_path('library')

def log_path() -> Path:
    return get_path('config', '.log')

def database_url() -> str:
    return str_path('config', 'database.db', rel=False)
    
def get_filename(*args: str | Path) -> list:
    home = root
    for arg in args: home = home / arg
    name, stem, suffix = home.name, home.stem, home.suffix

    if not suffix.isascii():
        stem += suffix
        suffix = ''
    elif stem.startswith('.') and suffix == '':
        stem, suffix = '', stem

    return [name, stem, suffix.lower()]

def is_music_file(path: str) -> bool:
    try:
        guess = filetype.guess(get_path(path))
    except:
        return True if get_path(path).suffix in SUFFIXES else False
    
    if not guess: return False
    if str(guess.mime).startswith('audio') or str(guess.mime).startswith('video'):
        return True
    else:
        return False

async def create_directory():
    if not config_dir().exists(): config_dir().mkdir()
    if not images_dir().exists(): images_dir().mkdir()
    if not library_dir().exists(): library_dir().mkdir()