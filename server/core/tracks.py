from core.images import *
from core.tracks import *
from core.logs import *
from model.model import *
from model.config import *
from tools.path import *
from tools.tags import *

global list_tags
list_tags = [column.name for column in tracks.columns]

class Tracks:
    def __init__(self, path: str | Path):
        self.path = get_path(path, rel=False)
        """Path, rel = False"""

        self.strpath = get_strpath(self.path)
        """str, rel = True"""

        self.tracks_id = get_hash(self.strpath)
        self.tracks_list = None

    async def insert(self):
        self.tracks_tags = await TagsTools(self.path, list_tags)
        if self.tracks_tags is None:
            logs.error("Failed to read tags. Is it a valid audio file?")
            return False
        
        async with db.transaction():
            await db.execute(tracks.insert().values(self.tracks_tags))
        logs.debug('Finished inserting tags.')

    async def delete(self, file_states: str):
        if file_states == 'dir':
            get_image_ids = await db.fetch_all(
                tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]).where(tracks.c.path.like(f'{self.strpath}%'))
            )

            # Removing all images from database with names starting from the image id
            image_path = get_path('data', 'images', rel=False)
            if get_image_ids:
                for image_id in get_image_ids:
                    for image_path_delete in image_path.glob(f"{image_id['imageid']}*"):
                        image_path_delete.unlink(missing_ok=True)
            else:
                return False

            # Removing all tracks from database with paths starting from the target directory
            await db.execute(tracks.delete().where(tracks.c.path.like(f'{self.strpath}%')))
        else:
            get_image_ids = await db.fetch_one(
                tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]).where(tracks.c.id == self.tracks_id)
            )
            if get_image_ids:
                image_path = get_path('data', 'images', rel=False)
                for image_file in image_path.glob(f"{get_image_ids['imageid']}"):
                    if image_file.is_file():
                        image_file.unlink(missing_ok=True)
            try:
                await db.execute(tracks.delete().where(tracks.c.id == self.tracks_id))
                logs.debug("track successfully deleted.")
            except:
                logs.error("Failed to delete track.")
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