from pathlib import Path
from tinytag import TinyTag
from pydantic_settings import BaseSettings
import re

ROOTDIR: Path = (Path.cwd().resolve()).parent

def get_path(*args: str | Path, rel: bool = False, create_dir: bool = False) -> Path:
    """
    Abstracts a path-like object or string path and returns it as a path-like object.
    Optionally creates the directory if it doesn't exist.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to False.
        create_dir (bool, optional): Create the directory if it doesn't exist, defaults to False.
    """
    
    home = ROOTDIR

    if create_dir:
        for arg in args: home = home / arg
        home.parent.mkdir(parents=True, exist_ok=True)
    else:
        for arg in args: home = home / arg
    
    return home.relative_to(ROOTDIR) if rel else home


def str_path(*args: str | Path, rel: bool = True) -> str:
    """
    Abstracts a path-like object or string path and returns it as a string.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to True.
    """

    home = ROOTDIR

    for arg in args: home = home / arg
    if rel: home = home.relative_to(ROOTDIR)

    return home.as_posix()


def get_filename(*args: str | Path) -> tuple[str, str, str]:
    home = ROOTDIR

    for arg in args: home = home / arg
    name, stem, suffix = home.name, home.stem, home.suffix

    if not suffix.isascii():
        stem += suffix
        suffix = ''
    elif stem.startswith('.') and suffix == '':
        stem, suffix = '', stem

    return [name, stem, suffix.lower()]


def is_supported_file(path: str) -> bool:
    if get_path(path).suffix in TinyTag.SUPPORTED_FILE_EXTENSIONS:
        return True
    else:
        return False


def create_dir(Config: BaseSettings) -> None:
    Config.DATADIR.mkdir(exist_ok=True)
    Config.LIBRARYDIR.mkdir(exist_ok=True)
    Config.ARTWORKDIR.mkdir(exist_ok=True)


def is_excluded_file(name: str) -> bool:
    """
    Check if a file should be excluded based on its name.
    """

    patterns = [
        r'.*Small.*',
        r'.*Cache.*',
        r'.*[{].*',
        r'.*cache.*',
        r'^\.',
        r'.*~$',
    ]

    for pattern in patterns:
        if re.search(pattern, name, re.IGNORECASE):
            return True
        
    return False
