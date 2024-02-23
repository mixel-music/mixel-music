from pathlib import Path, PurePath
import hashlib

SUFFIXES = [
    ".m4a", "mp4", ".3gp", ".m4b", ".m4p", "m4r", "m4v", ".aac",
    ".ogg", ".ogv", ".oga", ".ogx", ".ogm", ".spx", ".opus",
    ".dff", ".wsd", ".dsf",".mpc", ".mp+", ".mpp",
    ".wv", ".wvc", ".mp3", ".ac3", ".tak", ".tta",
    ".asf", ".wma", ".wmv", ".wav", ".wave",
    ".aiff", ".aif", ".aifc", ".flac",
]
root = (Path.cwd().resolve()).parent

def get_path(*args: str | Path, rel: bool = True) -> Path:
    """
    Abstracts a path-like object or string path within the application and returns it as a path-like object.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to True.
    """
    home = root
    for arg in args: home = home / arg
    if rel: home = home.relative_to(root)

    return home

def get_strpath(*args: str | Path, rel: bool = True) -> str:
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
    
def get_hash(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest().upper()
    
def get_name(*args: str) -> list:
    if not args: raise ValueError('get_name() needs a str or Path')

    home = root
    for arg in args: home = home / arg
        
    name = home.name
    stem = home.stem
    suffix = home.suffix

    if not suffix.isascii(): 
        stem += suffix
        suffix = ''
        return [name, stem, suffix]
    elif stem.startswith('.') and suffix == '':
        stem, suffix = '', stem

    return [name, stem, suffix]

def safe_int(value: int) -> int:
    try:
        return int(value)
    except ValueError:
        return 0

async def check_dir_init():
    data_path = get_path('data', rel=False)
    data_images_path = get_path('data', 'images', rel=False)
    library_path = get_path('library', rel=False)

    if data_path.exists() == False: data_path.mkdir()
    if data_images_path.exists() == False: data_images_path.mkdir()
    if library_path.exists() == False: library_path.mkdir()

async def check_suffixes(path: str | Path) -> bool:
    try:
        suffix = PurePath(path).suffix
    except:
        return False

    for check in SUFFIXES:
        if suffix == check:
            return True
        
    return False