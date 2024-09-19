import aiofiles
import asyncio
from concurrent.futures import ThreadPoolExecutor
from core.logger import *
from core.database import *
from tools.convert_value import *
from tools.path_handler import *
from tools.tags_handler import *
from models import *

semaphore = asyncio.Semaphore(5)

class Library:
    @staticmethod
    async def streaming(hash: str, range: str) -> tuple[bytes, dict[str, any]] | None:
        path = await hash_track_to_path(hash)
        track_info = await Library.get_track_info(hash)
        if not track_info: return

        track_mime = track_info['content_type']
        track_size = track_info['filesize']
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
                db_query = await conn.execute(
                    select(
                        Tracks.album,
                        Tracks.album_id,
                        Tracks.artist,
                        Tracks.artist_id,
                        Tracks.duration,
                        Tracks.title,
                        Tracks.track_id,
                    )
                    .order_by(Tracks.title.asc())
                    .offset(page)
                    .limit(item)
                )
                track_list = [dict(row) for row in db_query.mappings().all()]

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
    async def _get_track_info(id: str) -> dict:
        track_info = {}

        try:
            async with session() as conn:
                db_query = await conn.execute(
                    select(Tracks.__table__)
                    .where(Tracks.track_id == id)
                )
                track_info = dict(db_query.mappings().first())

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
                album_query = await conn.execute(
                    select(
                        Albums.album,
                        Albums.album_id,
                        Artists.artist.label('albumartist'),
                        Albums.albumartist_id,
                        Albums.year,
                    ).select_from(
                        join(
                            Albums, Artists,
                            Albums.albumartist_id == Artists.artist_id,
                        )
                    )
                    .order_by(Albums.album.asc())
                    .offset(page)
                    .limit(item)
                )
                album_list = [dict(row) for row in album_query.mappings().all()]

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
    async def _get_album_info(id: str) -> dict:
        album_info = {}

        try:
            async with session() as conn:
                album_query = await conn.execute(
                    select(
                        Albums.__table__,
                        Artists.artist.label('albumartist')
                    ).select_from(
                        join(
                            Albums, Artists,
                            Albums.albumartist_id == Artists.artist_id,
                        )
                    )
                    .where(Albums.album_id == id)
                )
                album_row = album_query.mappings().first()

                if album_row:
                    album_info = dict(album_row)
                    album_info['tracks'] = []

                    track_query = await conn.execute(
                        select(
                            Tracks.artist,
                            Tracks.artist_id,
                            Tracks.comment,
                            Tracks.duration,
                            Tracks.title,
                            Tracks.track_id,
                            Tracks.track_number,
                        )
                        .where(Tracks.album_id == id)
                        .order_by(Tracks.track_number.asc())
                    )
                    tracks = [dict(row) for row in track_query.mappings().all()]
                    album_info['tracks'].extend(tracks)

                return album_info
                
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
                db_query = await conn.execute(
                    select(Artists.__table__)
                    .order_by(Artists.artist.asc())
                    .offset(page)
                    .limit(item)
                )
                artist_list = [dict(row) for row in db_query.mappings().all()]
                
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
    async def _get_artist_info(id: str) -> dict:
        artist_info = {}

        try:
            async with session() as conn:
                # artist_id 또는 albumartist_id 일치하는 Tracks 항목
                track_query = await conn.execute(
                    select(Tracks.album_id)
                    .where(or_(Tracks.artist_id == id, Tracks.albumartist_id == id))
                )
                tracks_data = track_query.mappings().all()

                if tracks_data:
                    # 해당 아이템 있으면 album_id 사용하여 앨범 검색
                    album_ids = [track['album_id'] for track in tracks_data]
                    
                    album_from_tracks_query = await conn.execute(
                        select(
                            Albums.album,
                            Albums.album_id,
                            Albums.albumartist_id,
                            Albums.year,
                        )
                        .where(Albums.album_id.in_(album_ids))
                        .order_by(Albums.year.asc())
                    )
                    
                    albums_data = album_from_tracks_query.mappings().all()
                    albums_data = [dict(album) for album in albums_data]

                    if albums_data:
                        album = albums_data[0]
                        
                        # 앨범 albumartist_id 이용하여 아티스트 조회
                        artist_query = await conn.execute(
                            select(Artists.artist)
                            .where(Artists.artist_id == album['albumartist_id'])
                        )
                        artist_data = artist_query.mappings().first()

                        if artist_data:
                            artist_info = {
                                'artist': artist_data['artist'],
                                'artist_id': id,
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
                # Query to handle albums, excluding "Unknown Album"
                db_query = (
                    select(
                        Tracks.album,
                        Tracks.album_id,
                        Tracks.albumartist,
                        Tracks.albumartist_id,
                        Tracks.disc_total,
                        Tracks.track_total,
                        Tracks.year,
                        func.sum(Tracks.duration).label('duration_total'),
                        func.sum(Tracks.filesize).label('filesize_total'),
                    )
                    .where(
                        Tracks.album_id != '',
                    )
                    .group_by(
                        Tracks.album,
                        Tracks.album_id,
                        Tracks.albumartist,
                        Tracks.track_total,
                    )
                )

                db_result = await conn.execute(db_query)
                albums_data = db_result.all()

                # Insert each album data
                for alb in albums_data:
                    album_data = {
                        'album': alb.album,
                        'album_id': alb.album_id,
                        'albumartist_id': alb.albumartist_id,
                        'disc_total': alb.disc_total,
                        'duration_total': alb.duration_total,
                        'filesize_total': alb.filesize_total,
                        'year': alb.year,
                    }

                    await LibraryRepo.insert_album(conn, album_data)

                # Handle albums with "Unknown Album"
                unknown_query = (
                    select(
                        Tracks.album,
                        Tracks.album_id,
                        Tracks.artist,
                        Tracks.disc_total,
                        Tracks.track_total,
                        Tracks.year,
                        func.sum(Tracks.duration).label('duration_total'),
                        func.sum(Tracks.filesize).label('filesize_total'),
                    )
                    .where(Tracks.album == '')
                    .group_by(
                        Tracks.artist,
                        Tracks.directory,
                    )
                )

                unknown_result = await conn.execute(unknown_query)
                unknown_albums_data = unknown_result.all()

                # Insert each unknown album
                for alb in unknown_albums_data:
                    album_data = {
                        'album': alb.album,
                        'album_id': alb.album_id,
                        'albumartist_id': '',
                        'disc_total': alb.disc_total,
                        'duration_total': alb.duration_total,
                        'filesize_total': alb.filesize_total,
                        'year': alb.year,
                    }

                    await LibraryRepo.insert_album(conn, album_data)

                await conn.commit()

                # Remove albums that no longer have tracks
                albums_query = select(Albums.album_id)
                result = await conn.execute(albums_query)
                album_hash = {row.album_id for row in result}

                tracks_query = select(Tracks.album_id).distinct()
                result = await conn.execute(tracks_query)
                track_hash = {row.album_id for row in result}

                # Find albums present in Albums but not in Tracks
                orphan_albums = album_hash - track_hash

                for album_id in orphan_albums:
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
                        Tracks.albumartist,
                        Tracks.albumartist_id,
                        Tracks.artist,
                        Tracks.artist_id,
                    )
                    .distinct(Tracks.artist, Tracks.albumartist)
                )

                db_result = await conn.execute(db_query)
                artists_data = db_result.all()

                for track in artists_data:
                    # Initialize a set to avoid duplicating artists
                    artists_to_insert = set()

                    # If artist and albumartist are different, insert both
                    if track.artist_id != track.albumartist_id:
                        artists_to_insert.add((track.artist, track.artist_id))
                        artists_to_insert.add((track.albumartist, track.albumartist_id))
                    else:
                        # If artist and albumartist are the same, insert only one
                        artists_to_insert.add((track.artist, track.artist_id))

                    # Insert each unique artist/albumartist into the database
                    for artist_name, artist_id in artists_to_insert:
                        artist_data = {
                            'artist': artist_name,
                            'artist_id': artist_id,
                        }
                        await LibraryRepo.insert_artist(conn, artist_data)

                await conn.commit()

                # Remove artists that no longer have albums
                artists_query = select(Artists.artist_id)
                result = await conn.execute(artists_query)
                artist_hash = {row.artist_id for row in result}

                track_artists_query = (
                    select(Tracks.artist_id).distinct()
                    .union_all(
                        select(Tracks.albumartist_id).distinct()
                    )
                )
                result = await conn.execute(track_artists_query)
                track_artist_ids = {row.artist_id for row in result}

                orphan_artists = artist_hash - track_artist_ids

                for artist_id in orphan_artists:
                    logs.debug("Removing Artist %s", artist_id)
                    await LibraryRepo.delete_artist(conn, artist_id)

                await conn.commit()

        except Exception as error:
            logs.error("Failed to refresh artist list, %s", error)
            await conn.rollback()



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