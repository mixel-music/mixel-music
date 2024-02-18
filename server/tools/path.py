from pathlib import Path
import mimetypes
import aiofiles
import hashlib

root = (Path.cwd().resolve()).parent

def get_path(*args: str | Path, is_rel: bool = True, is_str: bool = True) -> str | Path:
    """
    애플리케이션의 루트 디렉터리, 디렉터리 및 파일 경로를 추상화하는 함수.

    Args:
        *args (str, Path, optional): 디렉토리 혹은 파일명. Defaults to the app root dir.
        is_rel (bool, optional): 루트 디렉토리에 대한 상대 경로를 반환. Defaults to True.
        is_str (bool, optional): str 타입 반환, False 시 Path 타입 반환. Defaults to True.
    """
    home = root

    for arg in args:
        home = home / arg

    if is_rel:
        home = home.relative_to(root)
    if is_str:
        home = home.as_posix()

    return home
    
def get_hash(input_value: str) -> str:
    return hashlib.md5(input_value.encode()).hexdigest().upper()
    
def get_name(*args: str | Path) -> list:
    if not args:
        raise ValueError('get_name() needs a str or Path')
    home = root

    for arg in args:
        home = home / arg

    if not home.is_file():
        return None
        
    name = home.name
    stem = home.stem
    suffix = home.suffix

    if suffix == '' and stem.startswith('.'):
        stem = ''
        suffix = stem

    return [name, stem, suffix]

def get_mime(input_value: str | Path) -> bool:
    input_value = get_path(input_value, is_rel=False)
    mime_type, _ = mimetypes.guess_type(input_value)
    return mime_type is not None and mime_type.startswith('audio/')