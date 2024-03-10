from datetime import datetime
from infra.logging import *
from infra.session import *
from core.models import *
from tools.convert_values import *
from tools.tags_extractor import *
from tools.process_image import *
from tools.standard_path import *
import aiofiles

MAXIMUM_TASKS = 5
track_sem = asyncio.Semaphore(MAXIMUM_TASKS)
album_sem = asyncio.Semaphore(1)

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
            async with track_sem:
                await LibraryTask.add_track(conn, track_tags)
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(LibraryTask.add_album(conn, album_hash, track_tags))
                    tg.create_task(LibraryTask.add_artist(conn, artist_hash, track_tags))

            await conn.commit()


    @staticmethod
    async def update(path: str):
        print("test")
        # try:
        #     old_date = await db.fetch_one(
        #         select(Tracks.created_date).where(Tracks.path == path)
        #     )
        #     await Library.remove(path)
        #     await Library.create(path, old_date)
        # except Exception as error:
        #     logs.error("Failed to update track, %s", error)


    @staticmethod
    async def remove(path: str):
        print("test")
        try:
            async with session() as conn:
                async with track_sem:
                    await conn.execute(delete(Tracks).where(Tracks.path == path))
                    
                await conn.commit()
        except Exception as error:
            logs.error("Failed to remove track, %s", error)
            return False


    @staticmethod
    async def stream(path: str, range):
        track_info = await Library.get_tracks(path)
        if track_info:
            track_mime = track_info['mime']
            track_size = track_info.size
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
    async def get_images(hash: str, size: int | str):
        if size == 'orig':
            for orig_image in images_dir().glob(f"{hash}_orig*"):
                if orig_image.is_file(): return orig_image
        elif int(size) in IMAGE_SIZES:
            thumb_image = images_dir() / f"{hash}_{size}.{IMAGE_SUFFIX}"
            return thumb_image if thumb_image.is_file() else False
        else:
            return False
        

    @staticmethod
    async def get_tracks(path: str = None, num: int = 35):
        if not path:
            try:
                async with session() as conn:
                    track_list = await conn.execute(
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
                        .limit(500)
                    )
                    track_list = track_list.mappings().all()
                    return [dict(track) for track in track_list] if track_list else {}

            except Exception as error:
                logs.error("Failed to load track list, %s", error)
                return {}
        else:
            try:
                async with session() as conn:
                    result = await conn.execute(
                        select(Tracks.__table__).where(Tracks.path == path)
                    )
                    track_data = result.mappings().first()
                    return track_data if track_data else {}

            except Exception as error:
                logs.error("Failed to load the track tags, %s", error)
                return {}


    @staticmethod
    async def get_albums(hash: str = None, num: int = 35):
        if not hash:
            try:
                async with session() as conn:
                    album_list = await conn.execute(
                        select(
                            Albums.albumhash,
                            Albums.album,
                            Albums.albumartist,
                            Albums.imagehash,
                            Albums.year,
                            Albums.tracktotals,
                            Albums.disctotals,
                        )
                        .order_by(Albums.album.asc())
                        .limit(500)
                    )
                    album_list = album_list.mappings().all()
                return [dict(album) for album in album_list] if album_list else {}
            
            except Exception as error:
                logs.error("Failed to load album list, %s", error)
                return {}
        else:
            try:
                async with session() as conn:
                    album_data = await conn.execute(
                        select(Albums).where(Albums.albumhash == hash)
                    )
                    album_data = album_data.mappings().first()
                    return dict(album_data) if album_data else {}
            
            except Exception as error:
                logs.error("Failed to load the album data, %s", error)
                return {}


    @staticmethod
    async def get_artists(num: int = 35) -> dict:
        try:
            async with session() as conn:
                artist_list = await conn.execute(
                    select(Artists).order_by(Artists.artist.asc()).limit(num)
                )
                artist_list = artist_list.mappings().all()
            return [dict(artist) for artist in artist_list] if artist_list else {}
        
        except Exception as error:
            logs.error("Failed to load artist list, %s", error)
            return {}


    @staticmethod
    async def get_playlist(num: int = 35) -> dict:
        pass


class LibraryTask:
    @staticmethod
    async def add_track(conn: AsyncSession, tags: dict):
        try:
            await conn.execute(
                insert(Tracks).values(**tags)
            )
        except Exception as error:
            logs.error("Failed to insert track, %s", error)


    @staticmethod
    async def add_album(conn: AsyncSession, hash: str, tags: dict):
        async with album_sem:
            is_exist = await conn.execute(
                select(Albums).where(Albums.albumhash == hash)
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
                except Exception as error:
                    logs.error("Failed to insert album, %s", error)
                    return False

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
                except:
                    logs.error("Failed to load album data, %s", error)
                    return False

                if old_value:
                    new_value = LibraryTask.album_values(old_value, tags)
                    try:
                        await conn.execute(
                            update(Albums).where(Albums.albumhash == hash).values(**new_value)
                        )
                    except Exception as error:
                        logs.error("Failed to update album, %s", error)
                        return False


    @staticmethod
    async def add_artist(conn: AsyncSession, hash: str, tags: dict):
        async with album_sem:
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
                except Exception as error:
                    logs.error("Failed to insert artist, %s", error)


    @staticmethod
    def album_values(old: dict, tags: dict):
        return {
            'tracktotals': max(tags.get('tracktotals'), old.get('tracktotals')),
            'durationtotals': old.get('durationtotals') + tags.get('duration'),
            'sizetotals': old.get('sizetotals') + tags.get('size', 0),
            'imagehash': tags.get('imagehash') if not old.get('imagehash') else old.get('imagehash'),
            'musicbrainz_albumartistid': tags.get('musicbrainz_albumartistid') if not old.get('musicbrainz_albumartistid') else old.get('musicbrainz_albumartistid'),
            'musicbrainz_albumid': tags.get('musicbrainz_albumid') if not old.get('musicbrainz_albumid') else old.get('musicbrainz_albumid'),
        }