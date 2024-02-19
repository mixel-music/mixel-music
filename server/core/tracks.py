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
        self.path = get_path(path, rel=False)
        """Path, rel = False"""

        self.strpath = get_strpath(self.path)
        """str, rel = True"""

        self.tracks_id = get_hash(self.strpath)
        self.tracks_list = None

    async def upcert(self):
        self.tracks_list = await db.fetch_one(
            tracks.select().with_only_columns([tracks.c.id, tracks.c.createdate]).where(tracks.c.id == self.tracks_id)
        )
        
        if self.tracks_list and self.tracks_list['createdate']:
            create_date = self.tracks_list['createdate']
            is_upcert = True
        else:
            is_upcert = False

        self.tracks_tags = await TagsTools(self.path, list_tags)
        if self.tracks_tags is None:
            logs.error("Failed to read tags. Is it a valid audio file?")
            return False
        
        if is_upcert == False:
            async with db.transaction():
                await db.execute(tracks.insert().values(self.tracks_tags))
            logs.debug('Finished inserting tags.')
        else:
            self.tracks_tags['createdate'] = create_date

            async with db.transaction():
                await db.execute(tracks.update().values(self.tracks_tags).where(tracks.c.id == self.tracks_id))
            logs.debug('Finished updating tags.')

    async def delete(self, file_states: str):
        print(self.strpath)
        if file_states == 'file':
            get_image_ids = await db.fetch_one(
                tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]).where(tracks.c.id == self.tracks.id)
            )
            if get_image_ids:
                image_id = get_image_ids['imageid']
                image_path = get_path('data', 'images', rel=False)
                for image_file in image_path.glob(f"{image_id}"):
                    if image_file.is_file():
                        image_file.unlink(missing_ok=True)
            try:
                await db.execute(tracks.delete().where(tracks.c.id == self.tracks_id))
                logs.debug("track successfully deleted.")
            except:
                logs.error("Failed to delete track.")
                return False
            
        elif file_states == 'dir':
            get_image_ids = await db.fetch_all(
                tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]).where(tracks.c.path.like(f'{self.strpath}%'))
            )
            print(get_image_ids)

            # Removing all images from database with names starting from the image id
            image_path = get_path('data', 'images', rel=False)
            if get_image_ids:
                for image_id in get_image_ids:
                    image_path_target = image_id['imageid']
                    print(image_path_target)
                    for image_path_delete in image_path.glob(f"{image_path_target}*"):
                        if image_path_delete.is_file():
                            image_path_delete.unlink(missing_ok=True)
            else:
                return False

            # Removing all tracks from database with paths starting from the target directory
            await db.execute(tracks.delete().where(tracks.c.path.like(f'{self.strpath}%')))

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