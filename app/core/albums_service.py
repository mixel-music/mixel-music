from core.convert_tools import *
from core.extract_tags import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

class AlbumsService:
    def __init__(
        self,
        name: str,
        albumartist: str,
        release_year: int,
        total_discnumber: int,
        musicbrainz_albumartistid: str,
        musicbrainz_albumid: str,
    ):
        self.name = name
        self.albumartist = albumartist
        self.release_year = release_year
        self.total_discnumber = total_discnumber
        self.musicbrainz_albumartistid = musicbrainz_albumartistid
        self.musicbrainz_albumid = musicbrainz_albumid
        
        self.albumid = get_hash_str(
            name + albumartist +
            str(release_year) +
            str(total_discnumber) +
            str(musicbrainz_albumartistid) +
            str(musicbrainz_albumid)
        )


    async def create(self, imageid: str, duration: int, size: int):
        try:
            await db.execute(
                albums.insert().values(
                    albumartist=self.albumartist,
                    albumid=self.albumid,
                    imageid=imageid,
                    name=self.name,
                    release_year=self.release_year,
                    total_discnumber=self.total_discnumber,
                    total_duration=duration,
                    total_size=size,
                    musicbrainz_albumartistid=self.musicbrainz_albumartistid,
                    musicbrainz_albumid=self.musicbrainz_albumid,
                )
            )
        except Exception as error:
            logs.error("Failed to insert album, %s", error)


    async def update(self):
        pass


    async def remove(self):
        try:
            await db.execute(
                albums.delete().where(
                    albums.c.name == self.name,
                    albums.c.albumartist == self.albumartist,
                )
            )
        except Exception as error:
            logs.error("Failed to remove album, %s", error)
            return False


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
            ).order_by(albums.c.name.asc()).limit(500) # Debug
        )
        if albums_select: [albums_data.append(dict(tag)) for tag in albums_select]
        return albums_data
    

    @staticmethod
    async def info(name: str, albumartist: str) -> dict:
        try:
            album_info = await db.fetch_one(
                albums.select().where(
                    albums.c.name == name,
                    albums.c.albumartist == albumartist,
                )
            )
            if album_info:
                return dict(album_info)
        except Exception as error:
            logs.error("Failed to load the album information, %s", error)
        return {}