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
        self.music = music.select().where(music.c.id == self.id)
        self.music = await database.fetch_one(self.music)
        
        if not self.abs_path.exists():
            if self.music:
                await self.delete()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if not self.music:
            await self.insert()
        else:
            return dict(self.music) if self.music is not None else {}

    async def insert(self):
        logging.debug("Found new track! path: %s, id: %s", self.str_path, self.id)
        self.tags = TagsTools(self.abs_path, list_tags)

        await database.execute(query=music.insert().values(self.tags))
        logging.debug('Insert music data complete!')

    async def update(self):
        query = music.select().with_only_columns([music.c.createdate]).where(music.c.id == self.id)
        result = await database.fetch_one(query)

        if result is None:
            return await self.insert()

        create_date = result['createdate']

        self.tags = TagsTools(self.abs_path, list_tags)
        self.tags['createdate'] = create_date

        query = music.update().where(music.c.path == self.str_path).values(self.tags)
        await database.execute(query)

    async def delete(self):
        try:
            query = music.delete().where(music.c.id == self.id)
            await database.execute(query=query)
        except Exception as e:
            logging.error(f"Error deleting track {self.id}: {e}")