from pathlib import Path

class PathTool:
    @staticmethod
    def get_path(*args: str) -> str:
        """
        By default, Returns the POSIX relative path as a string from the application root to the selected directory; 'args' can include any subdirectory or filename within.
        """
        root_dir = (Path(__file__).resolve()).parents[2]
        home_dir = root_dir
        
        if args is None: return (home_dir.relative_to(root_dir)).as_posix()
        for arg in args: home_dir = home_dir / arg

        return (home_dir.relative_to(root_dir)).as_posix()

    @staticmethod
    def abs_path(*args: str) -> Path:
        """
        By default, Returns the absolute path to the selected directory; 'args' can include any subdirectory or filename within.
        """
        root_dir = (Path(__file__).resolve()).parents[2]
        home_dir = root_dir
        
        if args is None: return home_dir
        for arg in args: home_dir = home_dir / arg

        return home_dir
    
    @staticmethod
    def file_names(*args: str) -> list:
        """
        Return the file name, file name without suffix and suffix.
        """
        root_dir = (Path(__file__).resolve()).parents[2]
        home_dir = root_dir

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