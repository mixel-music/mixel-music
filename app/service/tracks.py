from service.albums import *
from core.extract_tags import *
from core.image_task import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

list_tags = [column.name for column in tracks.columns]

class Tracks:
    def __init__(self, path: str):
        self.path = get_path(path, rel=False)
        self.strpath = get_strpath(path)

        self.tracks_id = get_hash(self.strpath)
        self.tracks_list = None

    async def create(self):
        self.tracks_tags = await TagsTools(self.path, list_tags)
        if self.tracks_tags is None:
            logs.debug("Failed to read tags. Is it a valid file?")
            return False
        
        try:
            await db.execute(tracks.insert().values(self.tracks_tags))
            logs.debug('Find new track! finished inserting tags.')

            duplicate_check = await db.fetch_one(
                albums.select().where(albums.c.id == self.tracks_id)
            )
            if not duplicate_check:
                albums_obj = Albums(self.tracks_tags['album'], self.tracks_tags['artist'], self.tracks_tags['year'])
                asyncio.create_task(albums_obj.init_album())

            return True
        except:
            logs.error("Failed to insert data into the database.")
            return False

    async def remove(self):
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