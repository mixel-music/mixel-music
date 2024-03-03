from core.convert_tools import *
from core.extract_tags import *
from infra.convert_image import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *
import aiofiles

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


    async def create(self, tags: dict):
        self.track_tags = tags
        if not self.track_tags:
            logs.debug("Failed to read tags. Is it a valid file?")
            return False
        try:
            await db.execute(tracks.insert().values(self.track_tags))
            return True
        except ValueError as error:
            logs.error("Failed to insert data into the database. %s", error)
            return False


    async def remove(self):
        try:
            await db.execute(tracks.delete().where(tracks.c.path == self.path))
        except Exception as error:
            logs.error("Failed to remove track, %s", error)
            return False


    @staticmethod
    async def list(num: int) -> list:
        track_tags = []
        tags_select = await db.fetch_all(
            tracks.select().with_only_columns(
                [
                    tracks.c.title,
                    tracks.c.artist,
                    tracks.c.album,
                    tracks.c.date,
                    tracks.c.trackid,
                    tracks.c.albumid,
                    tracks.c.artistid
                ]
            ).order_by(
                tracks.c.title.asc(),
            ).limit(500)
        )

        if tags_select: [track_tags.append(dict(tag)) for tag in tags_select]
        return track_tags


    @staticmethod
    async def info(path: str) -> dict:
        id = get_hash_str(path)
        track_info = {}
        
        try:
            track_data = await db.fetch_all(tracks.select().where(tracks.c.trackid == id))
            for data in track_data: track_info = dict(data)
        except Exception as error:
            logs.error("Failed to load the track information, %s", error)

        return track_info
    
    
    @staticmethod
    async def exists(path: str) -> bool:
        try:
            track_data = await db.fetch_one(tracks.select().where(tracks.c.path == path))
            return True if track_data else False
        except Exception as error:
            logs.debug("Failed to find track, %s", error)
            return False