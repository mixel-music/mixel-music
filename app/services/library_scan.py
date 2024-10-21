import asyncio
from models import Album, Artist, Track
from core.database import db_conn, select, func
from core.logging import logs
from repos.library import LibraryRepo


class LibraryScan:
    @staticmethod
    async def perform_all() -> None:
        alb = asyncio.create_task(LibraryScan.perform_albums())
        art = asyncio.create_task(LibraryScan.perform_artists())
        await alb, art


    @staticmethod
    async def perform_albums() -> None:
        async with db_conn() as conn:
            # Query to handle albums, excluding "Unknown Album"
            db_query = (
                select(
                    Track.album,
                    Track.album_id,
                    Track.albumartist,
                    Track.albumartist_id,
                    Track.disc_total,
                    Track.track_total,
                    Track.year,
                    func.sum(Track.duration).label('duration_total'),
                    func.sum(Track.filesize).label('filesize_total'),
                )
                .where(
                    Track.album_id != '',
                )
                .group_by(
                    Track.album,
                    Track.album_id,
                    Track.albumartist,
                    Track.track_total,
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

                await LibraryRepo(conn).insert_album(album_data)

            # Handle albums with "Unknown Album"
            unknown_query = (
                select(
                    Track.album,
                    Track.album_id,
                    Track.artist,
                    Track.disc_total,
                    Track.track_total,
                    Track.year,
                    func.sum(Track.duration).label('duration_total'),
                    func.sum(Track.filesize).label('filesize_total'),
                )
                .where(Track.album == '')
                .group_by(
                    Track.artist,
                    Track.directory,
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

                await LibraryRepo(conn).insert_album(album_data)

        async with db_conn() as conn:
            # Remove albums that no longer have tracks
            albums_query = select(Album.album_id)
            result = await conn.execute(albums_query)
            album_hash = {row.album_id for row in result}

            tracks_query = select(Track.album_id).distinct()
            result = await conn.execute(tracks_query)
            track_hash = {row.album_id for row in result}

            # Find albums present in Albums but not in Tracks
            orphan_albums = album_hash - track_hash

            for album_id in orphan_albums:
                logs.debug("Removing Album... (%s)", album_id)
                await LibraryRepo(conn).delete_album(album_id)


    @staticmethod
    async def perform_artists() -> None:
        async with db_conn() as conn:
            db_query = (
                select(
                    Track.albumartist,
                    Track.albumartist_id,
                    Track.artist,
                    Track.artist_id,
                )
                .distinct(Track.artist, Track.albumartist)
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
                    await LibraryRepo(conn).insert_artist(artist_data)

        async with db_conn() as conn:
            # Remove artists that no longer have albums
            artists_query = select(Artist.artist_id)
            result = await conn.execute(artists_query)
            artist_hash = {row.artist_id for row in result}

            track_artists_query = (
                select(Track.artist_id).distinct()
                .union_all(
                    select(Track.albumartist_id).distinct()
                )
            )
            result = await conn.execute(track_artists_query)
            track_artist_ids = {row.artist_id for row in result}

            orphan_artists = artist_hash - track_artist_ids

            for artist_id in orphan_artists:
                logs.debug("Removing Artist... (%s)", artist_id)
                await LibraryRepo(conn).delete_artist(artist_id)
