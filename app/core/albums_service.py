from core.convert_tools import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

class AlbumsService:
    def __init__(self, track: dict):
        self.track_info = {}
        for key, data in track:
            self.track_info[key] = data

    async def create(self):
        album_select = await db.fetch_one(
            albums.select().where(albums.c.albumid == self.track_info['albumid'])
        )
        if not album_select:
            await db.execute(
                albums.insert().values(
                    name=self.track_info['album'],
                    albumartist=self.track_info['albumartist'],
                    albumid=self.track_info['albumid'],
                    artist=self.track_info['artist'],
                    disctotal=self.track_info['disctotal'],
                    duration=self.track_info['duration'],
                    image_path=self.track_info['imageid'],
                    size=self.track_info['size'],
                    tracknumber=self.track_info['tracknumber'],
                    year_new=self.track_info['year'],
                    year_old=self.track_info['year'],
                )
            )

        else:
            pass

    async def update(self):
        pass

    async def remove(self):
        pass

    @staticmethod
    async def list(num: int) -> list:
        albums_data = []
        albums_select = await db.fetch_all(
            albums.select().with_only_columns(
                [
                    albums.c.name,
                    albums.c.albumartist,
                    albums.c.albumid,
                    albums.c.artist,
                    albums.c.image_path,
                    albums.c.tracknumber,
                    albums.c.year_new,
                ]
            ).order_by(
                albums.c.name.desc(),
                albums.c.artist.asc()
            ).limit(num)
        )

        if albums_select: [albums_data.append(dict(tag)) for tag in albums_select]

        return albums_data

    @staticmethod
    async def info(id: str) -> dict:
        pass