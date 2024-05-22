from datetime import datetime
import aiofiles
import asyncio

from core.models import *
from core.schema import *
from infra.config import *
from infra.database import *
from infra.loggings import *
from tools.convert_image import *
from tools.convert_value import *
from tools.path_handler import *
from tools.tags_handler import *

semaphore_lib = asyncio.Semaphore(5)
database_lock = asyncio.Semaphore(1)

class Library:
    @staticmethod
    async def create(path: str, date: datetime = datetime.now()) -> None:
        real_path = get_path(path)
        tags_table = [column.name for column in Tracks.__table__.columns]
        track_tags = await TagsHandler(path).extract_tags(tags_table)
        if not track_tags: return

        album_hash = get_hash_str(
            track_tags.get('album'),
            track_tags.get('albumartist'),
            track_tags.get('musicbrainz_albumid'),
            track_tags.get('year'),
        )

        if track_tags.get('album') == 'Unknown Album':
            album_hash = get_hash_str(
                album_hash,
                track_tags.get('imagehash'),
                track_tags.get('date')
            )

        artist_hash = get_hash_str(track_tags.get('artist'))
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

        async with session() as conn:
            async with semaphore_lib:
                logs.debug("Inserting \"%s\"", track_tags.get('title'))
                await Repository.insert_track(conn, track_tags)

                async with asyncio.TaskGroup() as tg:
                    tg.create_task(Repository.insert_album(conn, album_hash, track_tags))
                    tg.create_task(Repository.insert_artist(conn, artist_hash, track_tags))
            await conn.commit()


    @staticmethod
    async def update(path: str) -> None:
        async with session() as conn:
            async with database_lock:
                result = await conn.execute(
                    select(Tracks.created_date).where(Tracks.path == path)
                )
                result = result.scalar().first()
                await Library.remove(path)
                await Library.create(path, result.created_date)
            await conn.commit()


    @staticmethod
    async def remove(path: str) -> None:
        async with session() as conn:
            async with database_lock:
                album_hash = select(Tracks.albumhash).where(Tracks.path == path).alias('subquery')
                album_data = select(func.count()).select_from(Tracks).where(Tracks.albumhash.in_(select(album_hash.c.albumhash)))
                album_exist = await conn.execute(album_data)
                album_count = album_exist.scalar()
                if album_count == 1: await Repository.delete_album(conn, path)

                artist_hash = select(Tracks.artisthash).where(Tracks.path == path).alias('subquery')
                artist_data = select(func.count()).select_from(Tracks).where(Tracks.artisthash.in_(select(artist_hash.c.artisthash)))
                artist_exist = await conn.execute(artist_data)
                artist_count = artist_exist.scalar()
                if artist_count == 1: await Repository.delete_artist(conn, path)

                await Repository.delete_track(conn, path)
            await conn.commit()


    @staticmethod
    async def stream(hash: str, range):
        path = await hash_to_track(hash)
        track_info = await Library.get_tracks(hash)
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
    async def get_images(hash: str, size: int) -> Path:
        # if size == 'orig':
        #     for orig_image in conf.IMAGES_DIR.glob(f"{hash}_orig*"):
        #         if orig_image.is_file(): return orig_image
        if sanitize_num(size) in conf.IMG_SIZE:
            thumb_image = conf.IMG_DIR / f"{hash}_{size}.{conf.IMG_TYPE}"
            return thumb_image if thumb_image.is_file() else None
        else:
            return None


    @staticmethod
    async def get_tracks(hash: str = None, num: int = None):
        trk_list = []
        if not hash:
            try:
                async with session() as conn:
                    track_list = await conn.execute(select(Tracks.__table__).order_by(Tracks.title.asc()).limit(num))
                    track_list = track_list.mappings().all()

                for trk in track_list:
                    trk_dict = TrackListSchema(**trk).model_dump()
                    trk_list.append(trk_dict)

                return trk_list

            except OperationalError as err:
                logs.error("Failed to load tracks, %s", err)
                raise err
        else:
            try:
                path = await hash_to_track(hash)
                async with session() as conn:
                    result = await conn.execute(
                        select(Tracks.__table__).where(Tracks.path == path)
                    )
                    track_data = result.mappings().first()
                    return dict(track_data) if track_data else {}

            except OperationalError as err:
                logs.error("Failed to load track, %s", err)
                raise err
            

    @staticmethod
    async def get_albums(hash: str = None, num: int = None):
        try:
            async with session() as conn:
                if hash:
                    album_result = await conn.execute(
                        select(Albums.__table__).where(Albums.albumhash == hash)
                    )
                    album_data = album_result.mappings().first()
                    if album_data:
                        album_data = dict(album_data)
                        track_result = await conn.execute(
                            select(
                                Tracks.title,
                                Tracks.artist,
                                Tracks.hash,
                                Tracks.artisthash,
                                Tracks.tracknumber,
                            )
                            .where(Tracks.albumhash == hash)
                            .order_by(Tracks.tracknumber.asc())
                        )
                        album_data['tracks'] = [dict(track) for track in track_result.mappings().all()]
                        return album_data
                    else:
                        return {}
                else:
                    album_list = await conn.execute(
                        select(Albums.__table__).order_by(Albums.album.asc()).limit(num)
                    )
                    return [dict(album) for album in album_list.mappings().all()]
        except OperationalError as err:
            logs.error("Failed to load albums, %s", err)
            raise err
    

    @staticmethod
    async def get_artists(hash: str = None, num: int = None):
        art_list = []
        try:
            async with session() as conn:
                artist_list = await conn.execute(
                    select(Artists.__table__).order_by(Artists.artist.asc()).limit(num)
                )
                artist_list = artist_list.mappings().all()

                for art in artist_list:
                    art_dict = ArtistListSchema(**art).model_dump()
                    art_list.append(art_dict)

                return art_list
        
        except OperationalError as err:
            logs.error("Failed to load artists, %s", err)
            raise err


    @staticmethod
    async def get_playlists(hash: str = None, num: int = None):
        pass



class Repository:
    @staticmethod
    async def insert_track(conn: AsyncSession, tags: dict) -> None:
        try:
            await conn.execute(
                insert(Tracks).values(**tags)
            )
        except OperationalError as err:
            logs.error("Failed to insert track, %s", err)
            raise err


    @staticmethod
    async def delete_track(conn: AsyncSession, path: str) -> None:
        try:
            await conn.execute(delete(Tracks).where(Tracks.path == path))
        except OperationalError as err:
            logs.error("Failed to delete track, %s", err)
            raise err


    @staticmethod
    async def insert_album(conn: AsyncSession, hash: str, tags: dict) -> None:
        async with database_lock:
            is_exist = await conn.execute(
                select(Albums.__table__).where(Albums.albumhash == hash)
            )
            is_exist = is_exist.scalars().first()

            if not is_exist:
                try:
                    await conn.execute(insert(Albums).values(
                        albumhash=hash,
                        album=tags.get('album'),
                        albumartist=tags.get('albumartist'),
                        imagehash=tags.get('imagehash'),
                        date=tags.get('date'),
                        year=tags.get('year'),
                        durationtotals=tags.get('duration'),
                        tracktotals=tags.get('tracktotals'),
                        disctotals=tags.get('disctotals'),
                        sizetotals=tags.get('size'),
                        musicbrainz_albumartistid=tags.get('musicbrainz_albumartistid'),
                        musicbrainz_albumid=tags.get('musicbrainz_albumid'),
                    ))
                except OperationalError as err:
                    logs.error("Failed to insert album, %s", err)
                    raise err
            else:
                try:
                    old_value = await conn.execute(
                        select(
                            Albums.imagehash,
                            Albums.durationtotals,
                            Albums.tracktotals,
                            Albums.disctotals,
                            Albums.sizetotals,
                            Albums.musicbrainz_albumartistid,
                            Albums.musicbrainz_albumid,
                        ).where(Albums.albumhash == hash)
                    )
                    old_value = old_value.mappings().first()
                except OperationalError as err:
                    logs.error("Failed to load album, %s", err)
                    raise err

                if old_value:
                    new_value = album_values(old_value, tags)
                    try:
                        await conn.execute(
                            update(Albums).where(Albums.albumhash == hash).values(**new_value)
                        )
                    except OperationalError as err:
                        logs.error("Failed to update album, %s", err)
                        raise err


    @staticmethod
    async def delete_album(conn: AsyncSession, path: str) -> None:
        try:
            subquery = select(Tracks.albumhash).where(Tracks.path == path).alias('subquery')
            mainquery = delete(Albums.__table__).where(Albums.albumhash.in_(select(subquery.c.albumhash)))
            await conn.execute(mainquery)
            
        except OperationalError as err:
            logs.error("Failed to delete album, %s", err)
            raise err


    @staticmethod
    async def insert_artist(conn: AsyncSession, hash: str, tags: dict) -> None:
        async with database_lock:
            is_exist = await conn.execute(
                select(Artists).where(Artists.artisthash == hash)
            )
            is_exist = is_exist.scalars().first()
            if not is_exist:
                try:
                    await conn.execute(
                        insert(Artists).values(
                            artisthash=hash,
                            artist=tags.get('artist'),
                            imagehash='',
                        )
                    )
                except Exception as err:
                    logs.error("Failed to insert artist, %s", err)
                    raise err


    @staticmethod
    async def delete_artist(conn: AsyncSession, path: str) -> None:
        try:
            subquery = select(Tracks.artisthash).where(Tracks.path == path).alias('subquery')
            mainquery = delete(Artists.__table__).where(Artists.artisthash.in_(select(subquery.c.artisthash)))
            await conn.execute(mainquery)
            
        except OperationalError as err:
            logs.error("Failed to delete artist, %s", err)
            raise err