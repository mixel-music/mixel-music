from tools import *
from .database import *

global list_tags
list_tags = [column.name for column in music.columns]

class Tracks:
    def __init__(self, path: str):
        self.str_path = path
        self.abs_path = PathTools.abs(path)
        self.id = PathTools.get_md5_hash(path)

    async def lookup(self):
        if not self.abs_path.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        self.music = music.select().where(music.c.id == self.id)
        self.music = await database.fetch_one(self.music)

        if not self.music:
            await self.insert()
        else:
            return dict(self.music) if self.music is not None else {}

    async def insert(self):
        logging.debug("Found new track! path: %s, id: %s", self.str_path, self.id)
        self.tags = TagsTools(self.abs_path, list_tags)

        await database.execute(query=music.insert(), values=self.tags)
        logging.debug('Insert music data complete!')

    async def update(self):
        pass

    async def delete(self):
        try:
            query = music.delete().where(music.c.id == self.id)
            await database.execute(query=music.delete())
        except Exception as e:
            logging.error(f"Error deleting track {self.id}: {e}")