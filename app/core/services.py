from datetime import datetime
from infra.logging import *
from infra.session import *
from core.models import Tracks
from tools.convert_values import *
from tools.tags_extractor import *
from tools.process_image import *
from tools.standard_path import *
import aiofiles

sem = asyncio.Semaphore(20)

class Library:
    @staticmethod
    async def create(path: str):
        real_path = get_path(path)
        track_list = [column.name for column in Tracks.__table__.columns]
        track_tags = await ExtractTags(path).extract_tags(track_list)
        if not track_tags: return None

        track_tags.update({
            'albumhash': '',
            'artisthash': '',
            'created_date': datetime.now(),
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


    @staticmethod
    async def update(path: str):
        pass


    @staticmethod
    async def remove(path: str):
        pass


    @staticmethod
    async def stream(path: str, range):
        track_info = await Library.get_tracks(path)
        real_path = get_path(path)

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
    async def get_albums(path: str = None, num: int = None):
        return None


    @staticmethod
    async def get_artists(path: str = None, num: int = None):
        pass


    @staticmethod
    async def get_playlists(path: str = None, num: int = None):
        pass

# class LibraryHandler:
#     @staticmethod
#     async def create(path: str):
#         real_path = get_path(path)
#         track_list = [column.name for column in tracks.columns]
#         track_tags = await ExtractTags(path).extract_tags(track_list)
#         if not track_tags: return None

#         track_tags.update({
#             'albumid': '',
#             'artistid': '',
#             'create_date': datetime.now(),
#             'directory': str_path(real_path.parent),
#             'trackid': get_hash_str(path),
#             'path': path,
#             'size': real_path.stat().st_size,
#             'update_date': datetime.now(),
#         })
#         track_tags = dict(sorted(track_tags.items()))
#         track = TracksService(path)
        
#         async with sem:
#             try:
#                 await track.create(track_tags)
#             except Exception as error:
#                 logs.error("Failed to create track, %s", error)
#                 return False
            
#         album_check = await db.fetch_one(
#             albums.select().where(
#                 albums.c.name == track_tags.get('album'),
#             )
#         )
#         if not album_check:
#             album = AlbumsService(
#                 name=track_tags.get('album'),
#                 albumartist=track_tags.get('albumartist'),
#                 release_year=track_tags.get('year'),
#                 total_discnumber=track_tags.get('disctotal'),
#                 musicbrainz_albumartistid=track_tags.get('musicbrainz_albumartistid', ''),
#                 musicbrainz_albumid=track_tags.get('musicbrainz_albumid', ''),
#             )
#             await album.create(
#                 track_tags.get('imageid'),
#                 track_tags.get('duration'),
#                 track_tags.get('size'),
#             )


#     @staticmethod
#     async def update(path: str):
#         pass


#     @staticmethod
#     async def remove(path: str):
#         track = TracksService(path)
#         async with sem:
#             try:
#                 await track.remove()
#             except Exception as error:
#                 logs.error("Failed to remove track, %s", error)

#         album_check = await db.fetch_one(
#         albums.select().with_only_columns(albums.c.album, albums.c.albumartist).where(
#             albums.c.path == path,
#             )
#         )
#         if not album_check:
#             album = AlbumsService(
#                 name='',
#                 albumartist='',
#                 release_year=0,
#                 total_discnumber=0,
#                 musicbrainz_albumartistid='',
#                 musicbrainz_albumid='',
#             )
#             await album.remove(
#                 ''
#             )

# class TracksService:
#     def __init__(self, path: str):
#         self.path = path



#     async def create(self, tags: dict):
#         self.track_tags = tags
#         if not self.track_tags:
#             logs.debug("Failed to read tags. Is it a valid file?")
#             return False
#         try:
#             await db.execute(tracks.insert().values(self.track_tags))
#             return True
#         except ValueError as error:
#             logs.error("Failed to insert data into the database. %s", error)
#             return False


#     async def remove(self):
#         try:
#             await db.execute(tracks.delete().where(tracks.c.path == self.path))
#         except Exception as error:
#             logs.error("Failed to remove track, %s", error)
#             return False


#     @staticmethod
#     async def list(num: int) -> list:
#         track_tags = []
#         tags_select = await db.fetch_all(
#             tracks.select().with_only_columns(
#                 [
#                     tracks.c.title,
#                     tracks.c.artist,
#                     tracks.c.album,
#                     tracks.c.date,
#                     tracks.c.trackid,
#                     tracks.c.albumid,
#                     tracks.c.artistid
#                 ]
#             ).order_by(
#                 tracks.c.title.asc(),
#             ).limit(500)
#         )

#         if tags_select: [track_tags.append(dict(tag)) for tag in tags_select]
#         return track_tags


# class AlbumsService:
#     def __init__(
#         self,
#         name: str,
#         albumartist: str,
#         release_year: int,
#         total_discnumber: int,
#         musicbrainz_albumartistid: str,
#         musicbrainz_albumid: str,
#     ):
#         self.name = name
#         self.albumartist = albumartist
#         self.release_year = release_year
#         self.total_discnumber = total_discnumber
#         self.musicbrainz_albumartistid = musicbrainz_albumartistid
#         self.musicbrainz_albumid = musicbrainz_albumid
        
#         self.albumid = get_hash_str(
#             name + albumartist +
#             str(release_year) +
#             str(total_discnumber) +
#             str(musicbrainz_albumartistid) +
#             str(musicbrainz_albumid)
#         )


#     async def create(self, imageid: str, duration: int, size: int):
#         try:
#             await db.execute(
#                 albums.insert().values(
#                     albumartist=self.albumartist,
#                     albumid=self.albumid,
#                     imageid=imageid,
#                     name=self.name,
#                     release_year=self.release_year,
#                     total_discnumber=self.total_discnumber,
#                     total_duration=duration,
#                     total_size=size,
#                     musicbrainz_albumartistid=self.musicbrainz_albumartistid,
#                     musicbrainz_albumid=self.musicbrainz_albumid,
#                 )
#             )
#         except Exception as error:
#             logs.error("Failed to insert album, %s", error)


#     async def update(self):
#         pass


#     async def remove(self):
#         try:
#             await db.execute(
#                 albums.delete().where(
#                     albums.c.name == self.name,
#                     albums.c.albumartist == self.albumartist,
#                 )
#             )
#         except Exception as error:
#             logs.error("Failed to remove album, %s", error)
#             return False


#     @staticmethod
#     async def list(num: int) -> list:
#         albums_data = []
#         albums_select = await db.fetch_all(
#             albums.select().with_only_columns(
#                 [
#                     albums.c.name,
#                     albums.c.albumartist,
#                     albums.c.albumid,
#                     albums.c.imageid,
#                     albums.c.total_discnumber,
#                     albums.c.release_year,
#                 ]
#             ).order_by(albums.c.name.asc()).limit(500) # Debug
#         )
#         if albums_select: [albums_data.append(dict(tag)) for tag in albums_select]
#         return albums_data
    

#     @staticmethod
#     async def info(name: str, albumartist: str) -> dict:
#         try:
#             album_info = await db.fetch_one(
#                 albums.select().where(
#                     albums.c.name == name,
#                     albums.c.albumartist == albumartist,
#                 )
#             )
#             if album_info:
#                 return dict(album_info)
#         except Exception as error:
#             logs.error("Failed to load the album information, %s", error)
#         return {}