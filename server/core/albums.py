from core.logs import *
from model.model import *
from tools.path import *

class Albums:
    def __init__(self, path: str):
        self.path = get_path(path, rel=False)
        self.strpath = get_strpath(path)