from core.albums_service import *
from core.convert_tools import *
from core.extract_tags import *
from core.tracks_service import *
from infra.path_handler import *
from infra.setup_logger import *
from datetime import datetime

sem = asyncio.Semaphore(20)

class LibraryHandler:
    @staticmethod
    async def create(path: str):
        real_path = get_path(path)
        track_list = [column.name for column in tracks.columns]
        track_tags = await ExtractTags(path).extract_tags(track_list)
        if not track_tags: return None

        track_tags.update({
            'albumid': '',
            'artistid': '',
            'create_date': datetime.now(),
            'directory': str_path(real_path.parent),
            'trackid': get_hash_str(path),
            'path': path,
            'size': real_path.stat().st_size,
            'update_date': datetime.now(),
        })
        track_tags = dict(sorted(track_tags.items()))
        track = TracksService(path)
        
        async with sem:
            try:
                await track.create(track_tags)
            except Exception as error:
                logs.error("Failed to create track, %s", error)
                return False
            
        album_info = await AlbumsService.info(
            name=track_tags.get('album'),
            albumartist=track_tags.get('albumartist'),
        )
            
        if album_info == {}:
            album = AlbumsService(
                name=track_tags.get('album'),
                albumartist=track_tags.get('albumartist'),
                release_year=track_tags.get('year'),
                total_discnumber=track_tags.get('disctotal'),
                musicbrainz_albumartistid=track_tags.get('musicbrainz_albumartistid', ''),
                musicbrainz_albumid=track_tags.get('musicbrainz_albumid', ''),
            )
            await album.create(
                track_tags.get('imageid'),
                track_tags.get('duration'),
                track_tags.get('size'),
            )


        # # Album
        # if not await AlbumsService.info(
        #     name=track_info.get('album'),
        #     albumartist=track_info.get('albumartist'),
        #     total_discnumber=track_info.get('disctotal'),
        # ):
        #     album = AlbumsService(
        #         name=track_info.get('album'),
        #         albumartist=track_info.get('albumartist'),
        #         total_discnumber=track_info.get('disctotal'),
        #         imageid=track_info.get('imageid'),
        #     )
        #     try:
        #         await album.create()
        #     except Exception as error:
        #         logs.debug("Error: %s", error)
        #         return False
                
        # # Artist


    @staticmethod
    async def update(path: str):
        pass


    @staticmethod
    async def remove(path: str):
        track = TracksService(path)
        async with sem:
            try:
                await track.remove()
            except Exception as error:
                logs.error("Failed to remove track, %s", error)


    @staticmethod
    async def images(image_id: str, size: int | str):
        image_dir = images_dir()
    
        if size == 'orig':
            for orig_image in image_dir.glob(f"{image_id}_orig*"):
                if orig_image.is_file(): return orig_image
        elif int(size) in IMAGE_SIZES:
            thumb_image = image_dir / f"{image_id}_{size}.{IMAGE_SUFFIX}"
            return thumb_image if thumb_image.is_file() else False
        else:
            return False