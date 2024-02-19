from fastapi import HTTPException, status
from core.images import *
from core.tracks import *
from core.logs import *
from model.model import *
from tools.path import *
from tools.tags import *

global list_tags
list_tags = [column.name for column in tracks.columns]

class TracksObject:
    def __init__(self, path: str | Path):
        self.path = get_path(path, rel=False)
        self.strpath = get_strpath(self.path)
        self.tracks_list = None
        self.tracks_id = get_hash(self.strpath)

    async def insert(self):
        self.tracks_list = await db.fetch_one(
            tracks.select().with_only_columns(
                [
                    tracks.c.id,
                    tracks.c.createdate
                ]
            ).where(
                tracks.c.id == self.tracks_id
            )
        )
        
        if self.tracks_list:
            logs.debug("Find tags in database, skip inserting.")
            return False

        logs.debug("Find new track! Inserting tags...")
        self.tracks_tags = await TagsTools(self.path, list_tags)

        if self.tracks_tags is None:
            logs.error("Failed to read tags. Is it a valid audio file?")
            return False
        
        await db.execute(query=tracks.insert().values(self.tracks_tags))
        logs.debug('Finished inserting tags.')

    async def update(self):
        self.tracks_list = await db.fetch_one(
            tracks.select().with_only_columns([tracks.c.id, tracks.c.createdate]).where(tracks.c.id == self.tracks_id)
        )
        
        create_date = self.tracks_list['createdate']
        self.tracks_tags = await TagsTools(self.path, list_tags)
        
        if self.tracks_tags is None:
            logs.error("Failed to read tags. Is it a valid audio file?")
            return False
        
        self.tracks_tags['createdate'] = create_date

        await db.execute(query=tracks.insert().values(self.tracks_tags))
        logs.debug('Finished updating tags.')

    async def delete(self):
        is_image = await db.fetch_one(tracks.select().with_only_columns([tracks.c.imageid]).where(tracks.c.id == self.tracks_id))

        if is_image[0] != '':
            image_id = is_image['imageid']
            image_path = get_path('data', 'images', rel=False, is_str=False)

            for image_file in image_path.glob(f"{image_id}*"):
                if image_file.is_file():
                    image_file.unlink(missing_ok=True)

        try:
            await db.execute(tracks.delete().where(tracks.c.id == self.tracks_id))
            logs.debug("Completed deleting track.")

        except Exception as delete_error:
            logs.error(f"Failed to remove track '{self.tracks_id}': {delete_error}")
            return False

    @staticmethod
    async def get_list(num: int = 36) -> list:
        tracks_tags = []
        tracks_tags_select = await db.fetch_all(
            tracks.select().with_only_columns(
                [
                    tracks.c.title,
                    tracks.c.artist,
                    tracks.c.album,
                    tracks.c.year,
                    tracks.c.id,
                    tracks.c.albumid,
                    tracks.c.artistid
                ]
            )
        )

        if not tracks_tags_select:
            return tracks_tags

        for tag in tracks_tags_select:
            tracks_tags.append(dict(tag))

        return tracks_tags

    @staticmethod
    async def get_info(id: str) -> dict:
        tracks_data = []
        tracks_data_select = await db.fetch_all(tracks.select().where(tracks.c.id == id))

        if not tracks_data_select:
            logs.debug("Failed to load track info.")

            return tracks_data

        for data in tracks_data_select:
            tracks_data = dict(data)

        return tracks_data