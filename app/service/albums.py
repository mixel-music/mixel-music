import datetime
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *

class Albums:
    def __init__(self, album: str, artist: str, year: int):
        self.album_hash = get_hash(f"{album}-{artist}-{year}")
        self.album_name = album
        self.artist = artist
        self.album_artist = artist
        self.album_year = year

    async def init_album(self):
        """
        Create and insert a new album object. At least one track is required to create an album.
        """
        get_info = await db.fetch_all(
            tracks.select().with_only_columns(
                tracks.c.albumid,
                tracks.c.artist,
                tracks.c.artistid,
                tracks.c.imageid,
                tracks.c.date,
                tracks.c.dir,
                tracks.c.duration,
            ).where(tracks.c.albumid == self.album_hash)
        )

        if get_info:
            total_duration = 0
            total_size = 0
            track_numbers = len(get_info)
            earliest_date = ''
            latest_date = ''
            directories = ''

            for track_info in get_info:
                total_duration += track_info.duration
                track_date = track_info.date

            await db.execute(
                albums.insert().values(
                    id=self.album_hash,
                    name=self.album_name,
                    artist=self.artist,
                    artistid=get_hash(self.artist),
                    albumartist=self.album_artist,
                    albumartistid=get_hash(self.album_artist),
                    tracknumber=track_numbers,
                    size=total_size,
                    createdate=datetime.datetime.now(),
                    duration=total_duration,
                    dateafter=earliest_date,
                    datebefore=latest_date,
                    dir=directories,
                    yearafter=0,
                    yearbefore=0,
                    imagepath='',
                    imageid=get_info[0]['imageid'],
                )
            )

            logs.debug("Creating new album...")

    async def insert_track(self):
        pass

    async def remove_track(self):
        pass

    async def get_info(self):
        pass