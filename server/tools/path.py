from pathlib import Path, PurePath
import aiofiles
import hashlib

root = (Path.cwd().resolve()).parent

def get_path(*args: str | Path, rel: bool = True) -> Path:
    """
    애플리케이션 내 경로를 추상화 및 Path로 반환하는 함수.

    Args:
        *args (str | Path, optional): Directory or filename, Defaults to the app root dir.
        rel (bool, optional): 애플리케이션 루트에 대한 상대 경로 반환. Defaults to True.
    """
    home = root
    for arg in args: home = home / arg
    if rel: home = home.relative_to(root)

    return home

def get_strpath(*args: str | Path, rel: bool = True) -> str:
    """
    애플리케이션 내 경로를 추상화 및 str로 반환하는 함수.

    Args:
        *args (str | Path, optional): Directory or filename, Defaults to the app root dir.
        rel (bool, optional): 애플리케이션 루트에 대한 상대 경로 반환. Defaults to True.
    """
    home = root
    for arg in args: home = home / arg
    if rel: home = home.relative_to(root)

    return home.as_posix()
    
def get_hash(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest().upper()
    
def get_name(*args: str | Path) -> list:
    """
    [0]: (name).(suffix), [1]: (name), [2]: .(suffix)
    """
    if not args: raise ValueError('get_name() needs a str or Path')

    home = root
    for arg in args: home = home / arg
    if not home.is_file(): return None
        
    name = home.name
    stem = home.stem
    suffix = home.suffix

    if suffix == '' and stem.startswith('.'): stem, suffix = '', stem
    return [name, stem, suffix]

def create_dir_init():
    data_path = get_path('data', rel=False)
    data_images_path = get_path('data', 'images', rel=False)
    library_path = get_path('library', rel=False)

    if data_path.exists() == False: data_path.mkdir()
    if data_images_path.exists() == False: data_images_path.mkdir()
    if library_path.exists() == False: library_path.mkdir()