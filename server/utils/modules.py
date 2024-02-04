from pathlib import Path
import os

def get_root_path() -> Path:
    """
    return project root dir location
    """
    return Path(__file__).resolve().parent.parent.parent