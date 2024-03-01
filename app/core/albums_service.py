from core.convert_tools import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

class AlbumsService:
    def __init__(self, name: str, albumartist: str, total_discnumber: int, imageid: str):
        self.name = name
        self.albumartist = albumartist
        self.total_discnumber = total_discnumber
        self.imageid = imageid

    async def create(self):
        await db.execute(
            albums.insert().values(
                name=self.name,
                albumartist=self.albumartist,
                albumid=get_hash_str(self.name + self.albumartist + str(self.total_discnumber)),
                total_discnumber=self.total_discnumber,
                total_duration=123,
                imageid=self.imageid,
                total_size=123,
                release_year=2024
            )
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
                    albums.c.imageid,
                    albums.c.total_discnumber,
                    albums.c.release_year,
                ]
            ).order_by(
                albums.c.name.asc()
            ).limit(num)
        )

        if albums_select: [albums_data.append(dict(tag)) for tag in albums_select]

        return albums_data

    @staticmethod
    async def info(name: str, albumartist: str, total_discnumber: int) -> dict:
        album_dict = {}
        try:
            album_info = await db.fetch_all(
                albums.select().where(
                    albums.c.name == name,
                    albums.c.albumartist == albumartist,
                    albums.c.total_discnumber == total_discnumber
                )
            )
            if album_info:
                for data in album_info: album_dict = dict(data)
            else: return None
        except Exception as error:
            logs.error("Failed to load the album information, %s", error)

        return None