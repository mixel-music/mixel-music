from core.extract_tags import *
from core.convert_data import *
from core.process_images import *
from infra.database import *
from infra.init_logger import *
from infra.handle_path import *
import aiofiles

list_tags = [column.name for column in tracks.columns]

class TracksService:
    def __init__(self, path: str):
        self.path = path

    async def stream(self, range):  
        track_info = await self.info(self.path)
        real_path = get_path(self.path)

        if track_info:
            track_mime = track_info['mime']
            track_size = track_info['size']
            track_chunk = int(track_size * 0.25)

            if range:
                track_range = range.replace("bytes=", "").split("-")
                track_start = int(track_range[0])
                track_end = int(track_range[1]) if track_range[1] else track_start + track_chunk
            else:
                track_start = 0
                track_end = track_start + track_chunk
            track_end = min(track_end, track_size - 1)

            async with aiofiles.open(real_path, mode="rb") as track_file:
                await track_file.seek(track_start)
                data = await track_file.read(track_end - track_start + 1)
                headers = {
                    'Content-Range': f'bytes {track_start}-{track_end}/{track_size}',
                    'Accept-Ranges': 'bytes',
                    'Content-Length': str(track_end - track_start + 1),
                    'Content-Type': track_mime
                }

                return data, headers
        else:
            raise LookupError('Failed to lookup the tags data.')

    async def create(self):
        self.track_tags = await extract_tags(self.path, list_tags)

        if not self.track_tags:
            logs.debug("Failed to read tags. Is it a valid file?")

            return False
        
        try:
            await db.execute(tracks.insert().values(self.track_tags))
            logs.debug('Find new track! finished inserting tags.')

            images = ProcessImages(self.path)
            asyncio.create_task(images.extract())

            return True
        
        except ValueError as error:
            logs.error("Failed to insert data into the database. %s", error)

            return False

    async def update(self):
        pass

    async def remove(self):
        pass

    @staticmethod
    async def list(num: int) -> list:
        track_tags = []
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
                tracks.c.track.asc()
            ).limit(num)
        )

        if tags_select: [track_tags.append(dict(tag)) for tag in tags_select]

        return track_tags

    @staticmethod
    async def info(path: str) -> dict:
        id = get_hash_str(path)
        track_info = {}

        try:
            track_data = await db.fetch_all(tracks.select().where(tracks.c.id == id))
        except:
            logs.error("Failed to load the track information.")

        for data in track_data: track_info = dict(data)
        return track_info

    """
    def __init__(self, path: str):
        self.path = get_path(path)
        self.strpath = str_path(path)

        self.tracks_id = get_hash_str(self.strpath)
        self.tracks_list = None

    async def create(self):
        self.tracks_tags = await extract_tags(self.path)
        if self.tracks_tags is None:
            logs.debug("Failed to read tags. Is it a valid file?")
            return False
        
        try:
            await db.execute(tracks.insert().values(self.tracks_tags))
            logs.debug('Find new track! finished inserting tags.')

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
    
        return get_path(result.path) if result else None"""