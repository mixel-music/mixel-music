from fastapi import HTTPException, status
from model.cls_images import *
from model.cls_tracks import *
from model.database import *
from tools.path import *
from tools.tags import *

global list_tags
list_tags = [column.name for column in music.columns]

class Tracks:
    def __init__(self, path: str):
        self.str_path = path
        self.abs_path = get_path(path, is_rel=False, is_str=False)
        self.id = get_hash(path)

    @staticmethod
    async def get_list(num: int = 36) -> list:
        tracks_list = []
        db_select = music.select().with_only_columns([music.c.title, music.c.artist, music.c.album, music.c.year, music.c.id, music.c.albumid, music.c.artistid])
        db_result = await database.fetch_all(db_select)

        if not db_result:
            return tracks_list

        for row in db_result:
            tracks_list.append(dict(row))

        return tracks_list
    
    @staticmethod
    async def get_info(id: str) -> dict:
        db_select = music.select().where(music.c.id == id)
        db_result = await database.fetch_all(db_select)

        if not db_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        for row in db_result:
            tracks_info = dict(row)

        return tracks_info

    async def lookup(self):
        self.music = music.select().where(music.c.id == self.id)
        self.music = await database.fetch_one(self.music)
        
        if not self.abs_path.exists():
            if self.music:
                await self.delete()

        if not self.music:
            await self.insert()
        else:
            return dict(self.music) if self.music is not None else {}

    async def insert(self):
        self.tags = await TagsTools(self.abs_path, list_tags)
        
        if not self.tags:
            logging.debug("Error: can't read audio metadata")
            return None
        elif not self.tags is None:
            await database.execute(query=music.insert().values(self.tags))
            logging.debug('Insert music data complete!')

            image = ImageManagement(self.str_path)
            await image.image_bin()
            await image.image_add()

        return None

    async def update(self):
        query = music.select().with_only_columns([music.c.createdate]).where(music.c.id == self.id)
        result = await database.fetch_one(query)

        if result is None:
            logging.debug("Error: can't read audio metadata")
            return None
        elif not result is None:
            create_date = result['createdate']

            self.tags = await TagsTools(self.abs_path, list_tags)
            self.tags['createdate'] = create_date

            query = music.update().where(music.c.path == self.str_path).values(self.tags)
            await database.execute(query)

        return None

    async def delete(self):
        query = music.select().with_only_columns([music.c.image_id]).where(music.c.id == self.id)
        result = await database.fetch_one(query)

        if not result:
            return None
        
        prefix = result['image_id']
        image_path = get_path('data', 'images', is_rel=False, is_str=False)

        for file in image_path.glob(f"{prefix}*"):
            if file.is_file():
                print(f"Removing file: {file}")
                file.unlink(missing_ok=True)

        try:
            query = music.delete().where(music.c.id == self.id)
            await database.execute(query=query)
        except Exception as e:
            logging.error(f"Error deleting track {self.id}: {e}")