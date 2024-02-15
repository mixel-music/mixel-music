from tools import *
from .database import *

global list_tags
list_tags = [column.name for column in music.columns]

class Tracks:
    def __init__(self, path: str):
        self.path = path
        self.tags = None
        self.id = None

    async def lookup_track(self):
        self.id = PathTools.get_id(self.path)
        find_id_select = music.select().where(music.c.id == self.id)
        find_id_result = await database.fetch_one(find_id_select)

        if not find_id_result:
            logging.debug("Found new track! path: %s, id: %s", self.path, self.id)
            await self.insert_track()
        else:
            logging.debug("Found music id from database! MD5: %s", self.id)

    @staticmethod
    async def info_track(id: str) -> dict:
        find_id_select = music.select().where(music.c.id == id)
        find_id_result = await database.fetch_one(find_id_select)

        if find_id_result is not None:
            return dict(find_id_result)
        else:
            return {}

    async def insert_track(self):
        abs_path = PathTools.abs_path(self.path)
        self.tags = TagsTools(abs_path, list_tags)

        await database.execute(query=music.insert(), values=self.tags)
        logging.debug('Insert music data complete!')

    async def update_track(self):
        pass

    async def delete_track(self):
        pass

class Albums:
    def __init__(self, path: str):
        self.path = path
        self.id = None

    async def find_album(self):
        pass

class Artists:
    def __init__(self, path: str):
        self.path = path
        self.id = None

    async def find_artist(self):
        pass

class Playlists:
    def __init__(self, path: str):
        self.path = path
        self.id = None
    
    async def find_playlist(self):
        pass