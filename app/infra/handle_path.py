from pathlib import Path
import filetype

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
    
def get_filename(*args: str | Path) -> list:
    if not args: raise ValueError('get_filename() needs a str or Path')

    home = root
    for arg in args: home = home / arg
    name, stem, suffix = home.name, home.stem, home.suffix

    if not suffix.isascii():
        stem += suffix
        suffix = ''
    elif stem.startswith('.') and suffix == '':
        stem, suffix = '', stem

    return [name, stem, suffix.lower()]

def get_filetype(path: str | Path) -> list:
    if not path: raise ValueError('get_filetype() needs a str or Path')

    type_check = filetype.guess(get_path(path))
    return [type_check.extension, type_check.mime] if type_check else None

async def create_directory():
    config_dir = get_path('config')
    config_images_dir = get_path('config', 'images')
    library_dir = get_path('library')

    if not config_dir.exists(): config_dir.mkdir()
    if not config_images_dir.exists(): config_images_dir.mkdir()
    if not library_dir.exists(): library_dir.mkdir()