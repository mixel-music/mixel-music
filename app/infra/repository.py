import asyncio
from core.models import *
from infra.config import *
from infra.database import *
from infra.loggings import *
from infra.repository import *
from tools.convert_value import *
from tools.path_handler import *

prevent_block = asyncio.Semaphore(1)

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
        async with prevent_block:
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
                    logs.error("Failed to load the album info, %s", err)
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
        async with prevent_block:
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
    async def delete_artist(conn: AsyncSession, path: str) -> None:
        try:
            subquery = select(Tracks.artisthash).where(Tracks.path == path).alias('subquery')
            mainquery = delete(Artists.__table__).where(Artists.artisthash.in_(select(subquery.c.artisthash)))
            await conn.execute(mainquery)
            
        except OperationalError as err:
            logs.error("Failed to delete artist, %s", err)
            raise err