from datetime import datetime
from infra.logging import *
from infra.session import *
from core.models import Tracks, Albums
from tools.convert_values import *
from tools.tags_extractor import *
from tools.process_image import *
from tools.standard_path import *
import aiofiles

sem = asyncio.Semaphore(20)

class Library:
    @staticmethod
    async def create(path: str, date: datetime = datetime.now()):
        real_path = get_path(path)
        track_list = [column.name for column in Tracks.__table__.columns]
        track_tags = await ExtractTags(path).extract_tags(track_list)
        if not track_tags: return None

        album_hash = get_hash_str(
            track_tags.get('album'),
            track_tags.get('albumartist'),
            track_tags.get('musicbrainz_albumid'),
            track_tags.get('year'),
        )
        track_tags.update({
            'albumhash': album_hash,
            'artisthash': get_hash_str(track_tags.get('artist')),
            'created_date': date,
            'updated_date': datetime.now(),
            'directory': str_path(real_path.parent),
            'size': real_path.stat().st_size,
            'hash': get_hash_str(path),
            'path': path,
        })
        track_tags = dict(sorted(track_tags.items()))
        
        async with sem:
            try:
                await db.execute(insert(Tracks).values(**track_tags))
            except Exception as error:
                logs.error("Failed to create track, %s", error)
                return False
            
        if not await Library.get_albums(album_hash):
            pass

    @staticmethod
    async def update(path: str):
        try:
            old_date = await db.fetch_one(
                select(Tracks.created_date).where(Tracks.path == path)
            )
            await Library.remove(path)
            await Library.create(path, old_date)
        except Exception as error:
            logs.error("Failed to update track, %s", error)


    @staticmethod
    async def remove(path: str):
        try:
            await db.execute(delete(Tracks).where(Tracks.path == path))
        except Exception as error:
            logs.error("Failed to remove track, %s", error)
            return False


    @staticmethod
    async def stream(path: str, range):
        track_info = await Library.get_tracks(path)
        if track_info:
            track_mime = track_info['mime']
            track_size = track_info['size']
            track_chunk = int(track_size * 0.25)
            real_path = get_path(path)

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
        

    @staticmethod
    async def images(hash: str, size: int | str):
        if size == 'orig':
            for orig_image in images_dir().glob(f"{hash}_orig*"):
                if orig_image.is_file(): return orig_image
        elif int(size) in IMAGE_SIZES:
            thumb_image = images_dir() / f"{hash}_{size}.{IMAGE_SUFFIX}"
            return thumb_image if thumb_image.is_file() else False
        else:
            return False
        

    @staticmethod
    async def get_tracks(path: str = None, num: int = None) -> dict:
        if not path:
            tracks = []
            try:
                list_tracks = await db.fetch_all(
                    select(
                        Tracks.title,
                        Tracks.album,
                        Tracks.artist,
                        Tracks.date,
                        Tracks.hash,
                        Tracks.albumhash,
                        Tracks.artisthash,
                    )
                    .order_by(Tracks.title.asc())
                    .limit(num)
                )
                if list_tracks:
                    for tag in list_tracks: tracks.append(dict(tag))
                    return tracks
                else:
                    return None
            except Exception as error:
                logs.error("Failed to load tracks list, %s", error)
        else:
            try:
                track_data = await db.fetch_one(
                    select(Tracks).where(Tracks.path == path)
                )
                if track_data:
                    return dict(track_data)
                else:
                    return None
            except Exception as error:
                logs.error("Failed to load the track information, %s", error)


    @staticmethod
    async def get_albums(hash: str = None, num: int = None):
        if not hash:
            albums = []
            try:
                list_albums = await db.fetch_all(
                    select(
                        Albums.albumhash,
                        Albums.album,
                        Albums.albumartist,
                        Albums.imagehash,
                        Albums.year,
                        Albums.tracktotals,
                        Albums.disctotals,
                    )
                    .order_by(Albums.title.asc())
                    .limit(num)
                )
                if list_albums:
                    for tag in list_albums: albums.append(dict(tag))
                    return albums
                else:
                    return None
            except Exception as error:
                logs.error("Failed to load albums list, %s", error)
        else:
            try:
                album_data = await db.fetch_one(
                    select(Albums).where(Tracks.hash == hash)
                )
                if album_data:
                    return dict(album_data)
                else:
                    return None
            except Exception as error:
                logs.error("Failed to load the album information, %s", error)


    @staticmethod
    async def get_artists(path: str = None, num: int = None):
        pass


    @staticmethod
    async def get_playlists(path: str = None, num: int = None):
        pass