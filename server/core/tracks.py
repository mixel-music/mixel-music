from core.images import *
from core.logs import *
from model.model import *
from tools.path import *
from tools.tags import *

list_tags = [column.name for column in tracks.columns]

class Tracks:
    def __init__(self, path: str):
        self.path = get_path(path, rel=False)
        self.strpath = get_strpath(path)

        self.tracks_id = get_hash(self.strpath)
        self.tracks_list = None

    async def insert(self):
        self.tracks_tags = await TagsTools(self.path, list_tags)
        if self.tracks_tags is None:
            logs.debug("Failed to read tags. Is it a valid file?")
            return False
        
        try:
            await db.execute(tracks.insert().values(self.tracks_tags))
            logs.debug('Finished inserting tags.')
            return True
        except:
            logs.error("Failed to insert data into the database.")
            return False

    async def delete(self, path_type: str):
        if path_type == 'dir':
            select_db = await db.fetch_all(
                tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]).where(tracks.c.path.like(f'{self.strpath}%'))
            )
            # Removing all images from database with names starting from the image id
            image_path = get_path('data', 'images', rel=False)
            if select_db:
                for result_db in select_db:
                    for image_path_delete in image_path.glob(f"{result_db['imageid']}*"):
                        image_path_delete.unlink(missing_ok=True)
            else:
                return False

            # Removing all tracks from database with dirs matching from the target directory
            await db.execute(tracks.delete().where(tracks.c.dir.like(f'{self.strpath}%')))
            logs.debug("Directory successfully deleted.")
        else:
            select_db = await db.fetch_one(
                tracks.select().with_only_columns([tracks.c.path, tracks.c.imageid]).where(tracks.c.id == self.tracks_id)
            )
            if select_db:
                image_path = get_path('data', 'images', rel=False)
                for image_file in image_path.glob(f"{select_db.imageid}"):
                    if image_file.is_file():
                        image_file.unlink(missing_ok=True)
            try:
                await db.execute(tracks.delete().where(tracks.c.id == self.tracks_id))
                logs.debug("Track successfully deleted.")
            except:
                logs.error("Failed to delete track.")
                return False

    @staticmethod
    async def get_list(num: int) -> list:
        tracks_tags = []
        tags_select = await db.fetch_all(
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
            ).order_by(
                tracks.c.album.desc(),
                tracks.c.tracknumber.asc()
            ).limit(num)
        )

        if tags_select: [tracks_tags.append(dict(tag)) for tag in tags_select]
        return tracks_tags

    @staticmethod
    async def get_info(id: str) -> dict:
        try:
            tracks_data = await db.fetch_all(tracks.select().where(tracks.c.id == id))
        except:
            logs.error("Failed to load the track information.")
            return dict()

        for data in tracks_data: tracks_info = dict(data)
        return tracks_info
    
    @staticmethod
    async def get_path(id: str) -> Path:
        try:
            result = await db.fetch_one(
                tracks.select().with_only_columns([tracks.c.path]).where(tracks.c.id == id)
            )
        except:
            logs.error("Failed to find ID from the database.")
            return False
    
        return get_path(result.path, rel=False) if result else None