from fastapi import HTTPException, status
from core.images import *
from core.tracks import *
from core.logs import *
from model.model import *
from tools.path import *
from tools.tags import *

global list_tags
list_tags = [column.name for column in tracks.columns]

class Tracks:
    def __init__(self, path: str | Path):
        self.real_path = get_path(path, is_rel=False, is_str=False)
        """is_rel = False, is_str = False"""
        self.path = get_path(self.real_path)
        """is_rel = True, is_str = True"""
        self.id = get_hash(path)

    async def lookup(self):
        self.music = tracks.select().where(tracks.c.id == self.id)
        self.music = await db.fetch_one(self.music)
        
        if not self.real_path.exists():
            if self.music:
                await self.delete()

        if not self.music:
            await self.insert()
        else:
            return dict(self.music) if self.music is not None else {}

    async def insert(self):
        self.tags = await TagsTools(self.real_path, list_tags)
        
        if not self.tags:
            logs.error("Failed to read tags. Is it a valid audio file?")

            return None
        elif not self.tags is None:
            await db.execute(query=tracks.insert().values(self.tags))
            logs.debug('Finished inserting music tags.')

            image = ImageManagement(self.path)
            await image.image_bin()
            await image.image_add()

        return None

    async def update(self):
        query = tracks.select().with_only_columns([tracks.c.createdate]).where(tracks.c.id == self.id)
        result = await db.fetch_one(query)

        if result is None:
            logs.error("Failed to read tags. Is it a valid audio file?")

            return None
        elif not result is None:
            create_date = result['createdate']

            self.tags = await TagsTools(self.real_path, list_tags)
            self.tags['createdate'] = create_date

            query = tracks.update().where(tracks.c.path == self.path).values(self.tags)
            await db.execute(query)

        return None

    async def delete(self):
        query = tracks.select().with_only_columns([tracks.c.image_id]).where(tracks.c.id == self.id)
        result = await db.fetch_one(query)

        if not result:
            return None
        
        prefix = result['image_id']
        image_path = get_path('data', 'images', is_rel=False, is_str=False)

        for file in image_path.glob(f"{prefix}*"):
            if file.is_file():
                file.unlink(missing_ok=True)

        try:
            query = tracks.delete().where(tracks.c.id == self.id)
            await db.execute(query=query)
        except Exception as e:
            logs.error(f"Failed to remove track '{self.id}': {e}")

    @staticmethod
    async def get_list(num: int = 36) -> list:
        tracks_list = []
        db_select = tracks.select().with_only_columns([tracks.c.title, tracks.c.artist, tracks.c.album, tracks.c.year, tracks.c.id, tracks.c.albumid, tracks.c.artistid])
        db_result = await db.fetch_all(db_select)

        if not db_result:
            return tracks_list

        for row in db_result:
            tracks_list.append(dict(row))

        return tracks_list
    
    @staticmethod
    async def get_info(id: str) -> dict:
        db_select = tracks.select().where(tracks.c.id == id)
        db_result = await db.fetch_all(db_select)

        if not db_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        for row in db_result:
            tracks_info = dict(row)

        return tracks_info