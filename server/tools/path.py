from pathlib import Path
import hashlib

global allow_suffix
allow_suffix = ['.mp3', '.flac', '.wav', '.m4a', '.mp4', '.alac', '.opus']

class PathTools:
    _root_dir = (Path.cwd().resolve()).parent

    @classmethod
    def std(cls, *args: str) -> str:
        """
        By default, Returns the POSIX relative path as a string from the application root to the selected directory; 'args' can include any subdirectory or filename within.
        """
        home_dir = cls._root_dir

        if args is None: return (home_dir.relative_to(cls._root_dir)).as_posix()
        for arg in args: home_dir = home_dir / arg

        return (home_dir.relative_to(cls._root_dir)).as_posix()

    @classmethod
    def abs(cls, *args: str) -> Path:
        """
        By default, Returns the absolute path to the selected directory; 'args' can include any subdirectory or filename within.
        """
        home_dir = cls._root_dir

        if args is None: return home_dir
        for arg in args: home_dir = home_dir / arg

        return home_dir
    
    @classmethod
    def get_md5_hash(cls, value: str) -> str:
        hash = hashlib.md5(value.encode()).hexdigest().upper()

        return hash
    
    @classmethod
    def get_filename(cls, *args: str) -> list:
        home_dir = cls._root_dir

        for arg in args:
            home_dir = home_dir / arg

        if not home_dir.is_file():
            return None
            
        file_name = home_dir.name
        file_stem = home_dir.stem
        file_suffix = home_dir.suffix
            
        if home_dir.suffix == '' and home_dir.stem.startswith('.'):
            file_stem = ''
            file_suffix = home_dir.stem

        return [file_name, file_stem, file_suffix]
    
    @staticmethod
    def is_music(value: Path) -> bool:
        if value.suffix in allow_suffix:
            return True
        else:
            return False