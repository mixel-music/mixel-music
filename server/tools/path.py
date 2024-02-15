from pathlib import Path
import hashlib

class PathTools:
    _root_dir = (Path.cwd().resolve()).parent

    @classmethod
    def get_path(cls, *args: str) -> str:
        """
        By default, Returns the POSIX relative path as a string from the application root to the selected directory; 'args' can include any subdirectory or filename within.
        """
        home_dir = cls._root_dir

        if args is None: return (home_dir.relative_to(cls._root_dir)).as_posix()
        for arg in args: home_dir = home_dir / arg

        return (home_dir.relative_to(cls._root_dir)).as_posix()

    @classmethod
    def abs_path(cls, *args: str) -> Path:
        """
        By default, Returns the absolute path to the selected directory; 'args' can include any subdirectory or filename within.
        """
        home_dir = cls._root_dir
        
        if args is None: return home_dir
        for arg in args: home_dir = home_dir / arg

        return home_dir
    
    @classmethod
    def file_names(cls, *args: str) -> list:
        """
        Return the file name, file name without suffix, and suffix.
        """
        home_dir = cls._root_dir

        if not args:
            raise ValueError('Empty parameters')

        for arg in args:
            home_dir = home_dir / arg

        if not home_dir.is_file():
            raise ValueError("Incorrect path")
        
        file_name = home_dir.name
        file_stem = home_dir.stem
        file_suffix = home_dir.suffix
        
        if home_dir.suffix == '' and home_dir.stem.startswith('.'):
            file_stem = ''
            file_suffix = home_dir.stem

        return [file_name, file_stem, file_suffix]
    
    @classmethod
    def get_id(cls, value: str) -> str:
        """
        Create and return MD5 string.
        """
        hash = hashlib.md5(value.encode()).hexdigest().upper()

        return hash