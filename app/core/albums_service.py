from core.convert_tools import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

class AlbumsService:
    def __init__(self, track: dict):
        self.track_info = track
        print(self.track_info)

    async def create(self):
        album_select = await db.fetch_one(
            albums.select().where(albums.c.albumid == self.track_info.get('albumid'))
        )
        # if not album_select:
        #     await db.execute(
        #         albums.insert().values(
        #             name=self.track_info.get('album', ''),
        #             albumartist=self.track_info.get('albumartist'),
        #             albumid=self.track_info.get('albumid'),
        #             artist=self.track_info.get('artist'),
        #             disctotal=self.track_info.get('disctotal'),
        #             duration=self.track_info.get('duration'),
        #             image_path=self.track_info.get('imageid'),
        #             size=self.track_info.get('size'),
        #             tracknumber=0,
        #             year_new=self.track_info.get('year'),
        #             year_old=self.track_info.get('year'),
        #         )
        #     )

        # else:
        #     logs.debug("Album already exists.")

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