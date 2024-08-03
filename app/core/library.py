import aiofiles
import asyncio

from core.models import *
from infra.config import *
from infra.loggings import *
from infra.database import *
from tools.convert_value import *
from tools.path_handler import *
from tools.save_artwork import *
from tools.tags_handler import *

semaphore = asyncio.Semaphore(5)

class Library:
    @staticmethod
    async def stream(hash: str, range) -> tuple[bytes, dict[str, any]] | None:
        path = await hash_to_track(hash)

        track_info = await Library.get_tracks(hash = hash)
        if not track_info: return

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

        logs.debug("Streaming \"%s\" (%s-%s)", track_info['title'], track_start, track_end)
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


    @staticmethod
    async def get_artwork(hash: str, size: int) -> Path:
        """
        hash: albumhash, size = 0: Original Artwork
        """

        if size == 0:
            for orig_artwork in conf.IMAGES_DIR.glob(f"{hash}_orig*"):
                if orig_artwork.is_file(): return orig_artwork

        if sanitize_int(size) in conf.IMG_SIZE:
            artwork_thumb = conf.IMG_DIR / f"{hash}_{size}.{conf.IMG_TYPE}"
            return artwork_thumb if artwork_thumb .is_file() else None
        else:
            return None


    @staticmethod
    async def get_tracks(page: int = None, num: int = None, hash: str = None) -> tuple[list[dict], dict]:
        if hash:
            return await Library._get_track(hash)
        else:
            return await Library._get_tracks(page, num)


    @staticmethod
    async def _get_tracks(page: int, num: int) -> list[dict]:
        try:
            async with session() as conn:
                query = select(
                    Tracks.hash,
                    Tracks.title,
                    Tracks.album,
                    Tracks.albumhash,
                    Tracks.artist,
                    Tracks.albumartist,
                ).order_by(
                    Tracks.title.asc()
                ).offset(page).limit(num)

                result = await conn.execute(query)
                track_list = [dict(row) for row in result.mappings().all()]

                return track_list
            
        except OperationalError as err:
            logs.error("Failed to load tracks, %s", err)
            raise err


    @staticmethod
    async def _get_track(hash: str) -> dict:
        try:
            path = await hash_to_track(hash)
            async with session() as conn:
                query = select(Tracks.__table__).where(Tracks.path == path)
                result = await conn.execute(query)
                track_data = result.mappings().first()

                return dict(track_data) if track_data else {}
            
        except OperationalError as err:
            logs.error("Failed to load track, %s", err)
            raise err


    @staticmethod
    async def get_albums(hash: str = None, num: int = None) -> tuple[dict, list[dict]]:
        if hash:
            return await Library._get_album(hash)
        else:
            return await Library._get_albums(num)


    @staticmethod
    async def _get_album(hash: str) -> dict:
        try:
            async with session() as conn:
                album_query = select(Albums.__table__).where(Albums.albumhash == hash)
                album_result = await conn.execute(album_query)
                album_data = album_result.mappings().first()
                
                if album_data:
                    album_data = dict(album_data)

                    tracks_query = select(
                        Tracks.hash,
                        Tracks.title,
                        Tracks.artist,
                        Tracks.artisthash,
                        Tracks.duration,
                        Tracks.albumhash,
                        Tracks.track,
                    ).where(Tracks.albumhash == hash).order_by(Tracks.track.asc())
                    tracks_result = await conn.execute(tracks_query)
                    album_data['tracks'] = [dict(track) for track in tracks_result.mappings().all()]

                    return album_data
                else:
                    return {}
                
        except OperationalError as err:
            logs.error("Failed to load album, %s", err)
            raise err


    @staticmethod
    async def _get_albums(num: int) -> list[dict]:
        try:
            async with session() as conn:
                query = select(Albums.__table__).order_by(Albums.album.asc()).limit(num)
                result = await conn.execute(query)
                album_list = [dict(row) for row in result.mappings().all()]
                return album_list
            
        except OperationalError as err:
            logs.error("Failed to load albums, %s", err)
            raise err


    @staticmethod
    async def get_artists(num: int = None) -> list[dict]:
        try:
            async with session() as conn:
                query = select(Artists.__table__).order_by(Artists.artist.asc()).limit(num)
                result = await conn.execute(query)
                artist_list = [dict(row) for row in result.mappings().all()]
                return artist_list
            
        except OperationalError as err:
            logs.error("Failed to load artists, %s", err)
            raise err


class LibraryTask:
    def __init__(self, path: str) -> None:
        self.path = path
        self.real_path = get_path(path)
        

    async def create_track(self) -> None:
        tags = await extract_tags(self.path)

        async with semaphore:
            async with session() as conn:
                try:
                    logs.debug("Inserting \"%s\"", tags.get('title'))
                    await LibraryRepo.insert_track(conn, tags)
                    await conn.commit()

                except Exception as error:
                    logs.error("Failed to create track: %s", error)
                    await conn.rollback()


    async def remove_track(self) -> None:
        async with semaphore:
            async with session() as conn:
                try:
                    logs.debug("Removing \"%s\"", self.path)
                    await LibraryRepo.remove_track(conn, self.path)
                    await conn.commit()

                except Exception as error:
                    logs.error("Failed to remove track: %s", error)
                    await conn.rollback()


    @staticmethod
    async def create_artwork(hash: str) -> None:
        try:
            async with session() as conn:
                query = select(Tracks.path).where(Tracks.albumhash == hash)
                result = await conn.execute(query)

                data = result.mappings().first()
                if data: data = dict(data)

                artwork = await extract_artwork(data.get('path'))
                if artwork:
                    await save_artwork(artwork, hash)
                else:
                    logs.debug("Failed to extract artwork.")
                    
        except Exception as error:
            logs.error('error %s', error)


    @staticmethod
    async def remove_artwork(hash: str) -> None:
        pass


    @staticmethod
    async def perform_albums() -> None:
        """
        Create / Remove Album
        """

        async with session() as conn:
            try:
                query = select(
                    Tracks.album,
                    Tracks.albumartist,
                    Tracks.tracktotal,
                    Tracks.disctotal,
                    Tracks.year,
                    func.sum(Tracks.duration).label('totalduration'),
                    func.sum(Tracks.size).label('totalsize')
                ).group_by(Tracks.album, Tracks.albumartist, Tracks.tracktotal)

                result = await conn.execute(query)
                albums_data = result.all()

                for album_data in albums_data:
                    album_str = f"{album_data.album}-{album_data.albumartist}-{album_data.tracktotal}-{album_data.year}"
                    albumhash = get_hash_str(album_str)
                    albumartist_hash = get_hash_str(album_data.albumartist)

                    new_album = {
                        'album': album_data.album,
                        'albumartist': album_data.albumartist,
                        'albumartisthash': albumartist_hash,
                        'albumhash': albumhash,
                        'durationtotals': album_data.totalduration,
                        'sizetotals': album_data.totalsize,
                        'tracktotals': album_data.tracktotal,
                        'disctotals': album_data.disctotal,
                    }

                    update_query = (
                        update(Tracks)
                        .where(
                            Tracks.album == album_data.album,
                            Tracks.albumartist == album_data.albumartist,
                            Tracks.tracktotal == album_data.tracktotal,
                            Tracks.year == album_data.year
                        )
                        .values(albumhash=albumhash)
                        .execution_options(synchronize_session="fetch")
                    )

                    await conn.execute(update_query)
                    await LibraryRepo.insert_album(conn, new_album)

                await conn.commit()

            except Exception as error:
                logs.error("Error, %s", error)

    
        # async with session() as conn:
        #     try:
        #         albums_query = select(Albums.albumhash)
        #         result = await conn.execute(albums_query)
        #         album_hash = {row.albumhash for row in result}

        #         tracks_query = select(Tracks.albumhash).distinct()
        #         result = await conn.execute(tracks_query)
        #         track_hash = {row.albumhash for row in result}

        #         find = album_hash - track_hash # 중복 없애고 set으로 차집합 연산
        #         for albumhash in find:
        #             logs.debug("Removing Album %s", albumhash)
        #             await LibraryRepo.remove_album(conn, albumhash)

        #     except Exception as error:
        #         logs.error("Failed to fetch untracked albums, %s", error)

    
    @staticmethod
    async def perform_artists() -> None:
        pass


class LibraryRepo:
    @staticmethod
    async def insert_track(conn: AsyncSession, tags: dict) -> bool:
        try:
            await conn.execute(
                insert(Tracks).values(**tags)
            )
            return True
        
        except OperationalError as error:
            logs.error("Failed to insert track, %s", error)
            raise


    @staticmethod
    async def insert_album(conn: AsyncSession, tags: dict) -> bool:
        try:
            await conn.execute(
                Insert(Albums).values(**tags).on_conflict_do_nothing()
            )
            return True
        
        except OperationalError as error:
            logs.error("Failed to insert album, %s", error)
            raise


    @staticmethod
    async def remove_track(conn: AsyncSession, path: str) -> bool:
        try:
            await conn.execute(
                delete(Tracks).where(
                    Tracks.path == path,
                )
            )
            return True
        
        except OperationalError as error:
            logs.error("Failed to remove track, %s", error)
            raise


    @staticmethod
    async def remove_album(conn: AsyncSession, hash: str) -> bool:
        try:
            await conn.execute(
                delete(Albums).where(
                    Albums.albumhash == hash,
                )
            )
            return True
        
        except OperationalError as error:
            logs.error("Failed to remove album, %s", error)
            raise