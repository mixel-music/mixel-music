from pathlib import Path
import filetype

root = (Path.cwd().resolve()).parent

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
        return True if str(guess.mime).startswith('audio') or str(guess.mime).startswith('video') else False
    except:
        return False

async def create_directory():
    if not config_dir().exists(): config_dir().mkdir()
    if not images_dir().exists(): images_dir().mkdir()
    if not library_dir().exists(): library_dir().mkdir()