import aiofiles
import asyncio
from concurrent.futures import ThreadPoolExecutor
from core.models import *
from core.logger import *
from core.database import *
from tools.convert_value import *
from tools.path_handler import *
from tools.tags_handler import *

semaphore = asyncio.Semaphore(5)

class Library:
    @staticmethod
    async def streaming(hash: str, range: str) -> tuple[bytes, dict[str, any]] | None:
        path = await hash_track_to_path(hash)
        track_info = await Library.get_track_info(hash)
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

        if track_start == 0:
            logs.debug("Playing \"%s\" (%s-%s)", track_info['title'], track_start, track_end)
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
    async def get_track_list(page: int, item: int) -> list[dict]:
        return await Library._get_track_list(item * (page - 1), item)


    @staticmethod
    async def get_track_info(hash: str) -> tuple[list[dict], dict]:
        return await Library._get_track_info(hash)


    @staticmethod
    async def _get_track_list(page: int, item: int) -> list[dict]:
        track_list = [{}]
        count = 0

        try:
            async with session() as conn:
                db_query = (
                    select(
                        Tracks.track_id,
                        Tracks.album_id,
                        Tracks.artist_id,
                        Tracks.title,
                        Tracks.album,
                        Tracks.artist,
                        Tracks.duration,
                    )
                    .order_by(Tracks.title.asc())
                    .offset(page)
                    .limit(item)
                )

                db_result = await conn.execute(db_query)
                track_list = [dict(row) for row in db_result.mappings().all()]

                count_query = select(func.count()).select_from(Tracks)
                count_result = await conn.execute(count_query)
                count = count_result.scalar_one()

        except OperationalError as error:
            logs.error("Failed to load track list, %s", error)

        return {
            'list': track_list,
            'total': count,
        }
    

    @staticmethod
    async def _get_track_info(hash: str) -> dict:
        track_info = {}

        try:
            path = await hash_track_to_path(hash)
            async with session() as conn:
                db_query = (
                    select(Tracks.__table__)
                    .where(Tracks.filepath == path)
                )

                db_result = await conn.execute(db_query)
                track_info = dict(db_result.mappings().first())

                return track_info
            
        except OperationalError as error:
            logs.error("Failed to load track info, %s", error)
            return track_info
        

    @staticmethod
    async def get_album_list(page: int, item: int) -> list[dict]:
        return await Library._get_album_list(item * (page - 1), item)


    @staticmethod
    async def get_album_info(hash: str) -> tuple[list[dict], dict]:
        return await Library._get_album_info(hash)


    @staticmethod
    async def _get_album_list(page: int, item: int) -> list[dict]:
        album_list = [{}]
        count = 0

        try:
            async with session() as conn:
                db_query = (
                    select(
                        Albums.album,
                        Albums.album_id,
                        Albums.albumartist,
                        Albums.albumartist_id,
                        Albums.year,
                    )
                    .order_by(Albums.album.asc())
                    .offset(page)
                    .limit(item)
                )

                db_result = await conn.execute(db_query)
                album_list = [dict(row) for row in db_result.mappings().all()]

                count_query = select(func.count()).select_from(Albums)
                count_result = await conn.execute(count_query)
                count = count_result.scalar_one()

        except OperationalError as error:
            logs.error("Failed to load album list, %s", error)

        return {
            'list': album_list,
            'total': count,
        }


    @staticmethod
    async def _get_album_info(hash: str) -> dict:
        album_info = {}

        try:
            async with session() as conn:
                album_query = select(Albums.__table__).where(Albums.album_id == hash)
                album_result = await conn.execute(album_query)
                album_info = album_result.mappings().first()

                if album_info:
                    album_info = dict(album_info)
                    track_query = (
                        select(
                            Tracks.track_id,
                            Tracks.artist_id,
                            Tracks.title,
                            Tracks.artist,
                            Tracks.track,
                            Tracks.disc,
                            Tracks.comment,
                            Tracks.duration
                        )
                        .order_by(Tracks.track.asc())
                        .where(Tracks.album_id == hash)
                    )

                    track_result = await conn.execute(track_query)
                    album_info['tracks'] = [dict(track) for track in track_result.mappings().all()]

                    return album_info
                
                else:
                    return {}
                
        except OperationalError as error:
            logs.error("Failed to load album info, %s", error)
            return album_info
        

    @staticmethod
    async def get_artist_list(page: int, item: int) -> list[dict]:
        return await Library._get_artist_list(item * (page - 1), item)


    @staticmethod
    async def get_artist_info(hash: str) -> tuple[list[dict], dict]:
        return await Library._get_artist_info(hash)


    @staticmethod
    async def _get_artist_list(page: int, item: int) -> list[dict]:
        artist_list = [{}]
        count = 0

        try:
            async with session() as conn:
                db_query = (
                    select(Artists.__table__)
                    .order_by(Artists.artist.asc())
                    .offset(page)
                    .limit(item)
                )

                db_result = await conn.execute(db_query)
                artist_list = [dict(row) for row in db_result.mappings().all()]
                
                count_query = select(func.count()).select_from(Artists)
                count_result = await conn.execute(count_query)
                count = count_result.scalar_one()

        except OperationalError as error:
            logs.error("Failed to load artist list, %s", error)

        return {
            'list': artist_list,
            'total': count,
        }
    

    @staticmethod
    async def _get_artist_info(hash: str) -> dict:
        artist_info = {}

        try:
            async with session() as conn:
                artist_query = select(Artists.__table__).where(Artists.artist_id == hash)
                artist_result = await conn.execute(artist_query)
                artist_info = artist_result.mappings().first()

                if artist_info:
                    artist_info = dict(artist_info)

                    album_query = (
                        select(Albums.__table__)
                        .where(Albums.albumartist_id == hash)
                        .order_by(Albums.year.desc())
                    )

                    album_result = await conn.execute(album_query)
                    albums_data = album_result.mappings().all()
                    logs.debug("%s", albums_data)

                    artist_info['albums'] = [dict(album) for album in albums_data]
                    
                    return artist_info
                else:
                    track_subquery = (
                        select(Tracks.albumartist_id)
                        .where(Tracks.artist_id == hash)
                        .subquery()
                    )
                    
                    album_from_tracks_query = (
                        select(Albums.__table__)
                        .where(Albums.albumartist_id.in_(select(track_subquery)))
                        .order_by(Albums.year.desc())
                    )

                    track_result = await conn.execute(album_from_tracks_query)
                    albums_data = track_result.mappings().all()
                    albums_data = [dict(album) for album in albums_data]

                    if albums_data:
                        album = albums_data[0]
                        artist_info = {
                            'artist_id': album.get('artist_id', ''),
                            'artist': album.get('albumartist', ''),
                            'albums': albums_data
                        }
                        return artist_info
                
            return {}
                
        except OperationalError as error:
            logs.error("Failed to load artist info, %s", error)
            return artist_info



class LibraryTask:
    def __init__(self, path: str) -> None:
        self.path = path
        self.tags = {}
        

    async def create_track(self) -> None:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            self.tags = await loop.run_in_executor(executor, extract_tags, self.path)

        if self.tags:
            async with semaphore:
                async with session() as conn:
                    try:
                        logs.debug("Inserting \"%s\"", self.tags.get('title'))
                        await LibraryRepo.insert_track(conn, self.tags)
                        await conn.commit()

                    except Exception as error:
                        logs.error("LibraryTask: Failed to create track: %s", error)
                        await conn.rollback()


    async def remove_track(self) -> None:
        async with semaphore:
            async with session() as conn:
                try:
                    logs.debug("Removing \"%s\"", self.path)
                    await LibraryRepo.delete_track(conn, self.path)
                    await conn.commit()

                except Exception as error:
                    logs.error("LibraryTask: Failed to remove track: %s", error)
                    await conn.rollback()



class LibraryScan:
    @staticmethod
    async def perform_all() -> None:
        alb = asyncio.create_task(LibraryScan.perform_albums())
        art = asyncio.create_task(LibraryScan.perform_artists())
        await alb, art

    @staticmethod
    async def perform_albums() -> None:
        try:
            async with session() as conn:
                # Query to handle albums excluding Unknown Album
                db_query = (
                    select(
                        Tracks.album,
                        Tracks.albumartist,
                        Tracks.artist,
                        Tracks.total_track,
                        Tracks.total_disc,
                        Tracks.year,
                        func.sum(Tracks.duration).label('total_duration'),
                        func.sum(Tracks.filesize).label('total_filesize'),
                    )
                    .where(Tracks.album != '')
                    .group_by(
                        Tracks.album,
                        Tracks.albumartist,
                        Tracks.total_track,
                    )
                )

                db_result = await conn.execute(db_query)
                albums_data = db_result.all()

                for alb in albums_data:
                    albumhash = hash_str(
                        f'{alb.album}-{alb.albumartist}-{alb.total_track}-{alb.year}'
                    )
                    albumartisthash = hash_str(alb.albumartist)

                    update_track = (
                        update(Tracks)
                        .where(
                            Tracks.album == alb.album,
                            Tracks.albumartist == alb.albumartist,
                            Tracks.total_track == alb.total_track,
                        )
                        .values(album_id=albumhash)
                        .execution_options(synchronize_session='fetch')
                    )

                    album_data = {
                        'album_id': albumhash,
                        'albumartist_id': albumartisthash,
                        'album': alb.album,
                        'albumartist': alb.albumartist,
                        'total_duration': alb.total_duration,
                        'total_filesize': alb.total_filesize,
                        'total_disc': alb.total_disc,
                        'year': alb.year,
                    }

                    await conn.execute(update_track)
                    await LibraryRepo.insert_album(conn, album_data)

                # Handle Unknown Album entries separately
                unknown_query = (
                    select(
                        Tracks.album,
                        Tracks.artist,
                        Tracks.total_track,
                        Tracks.total_disc,
                        Tracks.year,
                        func.sum(Tracks.duration).label('total_duration'),
                        func.sum(Tracks.filesize).label('total_filesize'),
                    )
                    .where(Tracks.album == '')
                    .group_by(
                        Tracks.album,
                        Tracks.artist,
                        Tracks.total_track,
                    )
                )

                unknown_result = await conn.execute(unknown_query)
                unknown_albums_data = unknown_result.all()

                for alb in unknown_albums_data:
                    albumhash = hash_str(
                        f'{alb.album}-{alb.artist}-{alb.total_track}-{alb.year}'
                    )
                    albumartisthash = hash_str(alb.artist)

                    update_track = (
                        update(Tracks)
                        .where(
                            Tracks.album == alb.album,
                            Tracks.artist == alb.artist,
                            Tracks.total_track == alb.total_track,
                        )
                        .values(album_id=albumhash)
                        .execution_options(synchronize_session='fetch')
                    )

                    album_data = {
                        'album_id': albumhash,
                        'albumartist_id': albumartisthash,
                        'album': alb.album,
                        'albumartist': alb.artist,
                        'total_duration': alb.total_duration,
                        'total_filesize': alb.total_filesize,
                        'total_disc': alb.total_disc,
                        'year': alb.year,
                    }

                    await conn.execute(update_track)
                    await LibraryRepo.insert_album(conn, album_data)

                await conn.commit()

                async with session() as conn:
                    albums_query = select(Albums.album_id)
                    result = await conn.execute(albums_query)
                    album_hash = {row.album_id for row in result}

                    tracks_query = select(Tracks.album_id).distinct()
                    result = await conn.execute(tracks_query)
                    track_hash = {row.album_id for row in result}

                    find = album_hash - track_hash # 중복 없애고 set으로 차집합 연산

                    for album_id in find:
                        logs.debug("Removing Album %s", album_id)
                        await LibraryRepo.delete_album(conn, album_id)

                    await conn.commit()

        except Exception as error:
            logs.error("Failed to refresh album list, %s", error)
            await conn.rollback()

    
    @staticmethod
    async def perform_artists() -> None:
        try:
            async with session() as conn:
                db_query = (
                    select(
                        Tracks.track_id,
                        Tracks.albumartist,
                    )
                    .distinct(Tracks.albumartist)
                    .order_by(Tracks.albumartist.asc())
                )

                db_result = await conn.execute(db_query)
                artists_data = db_result.all()

                # 아티스트, 앨범 아티스트 그대로, 아티스트는 변환 거친 해시, 앨범 아티스트는 그냥 해시
                # 앨범에는 앨범 아티스트와 앨범 아티스트 해시만 존재
                # 아티스트 목록에는 앨범 아티스트만 표시하되, 아티스트 해시가 달라도 앨범 아티스트 해시 동일하면 여기로

                for track in artists_data:
                    if track.albumartist:
                        artist_data = {
                            'artist': track.albumartist,
                            'artist_id': hash_str(track.albumartist),
                        }

                        await LibraryRepo.insert_artist(conn, artist_data)

                await conn.commit()

        except Exception as error:
            logs.error("Failed to refresh artist list, %s", error)
            await conn.rollback()

        async with session() as conn:
            artists_query = select(Artists.artist_id)
            result = await conn.execute(artists_query)
            artist_hash = {row.artist_id for row in result}

            albums_query = select(Tracks.albumartist_id).distinct()
            result = await conn.execute(albums_query)
            album_hash = {row.albumartist_id for row in result}

            find = artist_hash - album_hash

            for artist_id in find:
                logs.debug("Removing Artist %s", artist_id)
                await LibraryRepo.delete_artist(conn, artist_id)

            await conn.commit()



class LibraryRepo:
    @staticmethod
    async def insert_track(conn: AsyncSession, tags: dict) -> bool:
        try:
            await conn.execute(
                insert(Tracks).values(**tags)
            )
            return True
        
        except OperationalError as error:
            logs.error("LibraryRepo: Failed to insert track, %s", error)
            raise


    @staticmethod
    async def insert_album(conn: AsyncSession, tags: dict) -> bool:
        try:
            await conn.execute(
                Insert(Albums).values(**tags)
                .on_conflict_do_nothing()
            )
            return True
        
        except OperationalError as error:
            logs.error("LibraryRepo: Failed to insert album, %s", error)
            raise


    @staticmethod
    async def delete_track(conn: AsyncSession, path: str) -> bool:
        try:
            await conn.execute(
                delete(Tracks).where(Tracks.filepath == path)
            )
            return True
        
        except OperationalError as error:
            logs.error("LibraryRepo: Failed to delete track, %s", error)
            raise


    @staticmethod
    async def delete_album(conn: AsyncSession, hash: str) -> bool:
        try:
            await conn.execute(
                delete(Albums).where(Albums.album_id == hash)
            )
            return True
        
        except OperationalError as error:
            logs.error("LibraryRepo: Failed to delete album, %s", error)
            raise


    @staticmethod
    async def insert_artist(conn: AsyncSession, tags: dict) -> bool:
        try:
            await conn.execute(
                Insert(Artists).values(**tags)
                .on_conflict_do_nothing()
            )
            return True
        
        except OperationalError as error:
            logs.error("LibraryRepo: Failed to insert artist, %s", error)
            raise


    @staticmethod
    async def delete_artist(conn: AsyncSession, hash: str) -> bool:
        try:
            await conn.execute(
                delete(Artists).where(Artists.artist_id == hash)
            )
            return True
        
        except OperationalError as error:
            logs.error("LibraryRepo: Failed to delete artist, %s", error)
            raise