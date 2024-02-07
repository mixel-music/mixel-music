from pathlib import Path

global valid_extension_list
valid_extension_list = (
    ".mp3",
    ".m4a",
    ".mp4",
    ".flac",
    ".wav"
)

def get_absolute_path(*args) -> Path:
    absolute_path = Path(__file__).parents[2]

    if args is None: return absolute_path
    for arg in args: absolute_path = absolute_path / arg

    return absolute_path

def is_valid_extension(path: Path) -> bool:
    file_path = path
    file_extension = file_path.suffix.lower()

    if file_extension not in valid_extension_list:
        return False
    if not file_path.is_file(): 
        return False

    return True