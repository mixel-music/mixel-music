from core.albums_service import *
from core.convert_tools import *
from core.extract_tags import *
from core.tracks_service import *
from infra.path_handler import *
from infra.setup_logger import *

sem = asyncio.Semaphore(20)
class LibraryHandler:
    @staticmethod
    async def create(path: str):
        # Track
        track = TracksService(path)
        async with sem:
            try:
                await track.create()
            except Exception as error:
                logs.error("Failed to create track, %s", error)
                return False

        # common
        track_info = await TracksService.info(path)

        # Album
        if not await AlbumsService.info(
            name=track_info.get('album'),
            albumartist=track_info.get('albumartist'),
            total_discnumber=track_info.get('disctotal'),
        ):
            album = AlbumsService(
                name=track_info.get('album'),
                albumartist=track_info.get('albumartist'),
                total_discnumber=track_info.get('disctotal'),
                imageid=track_info.get('imageid'),
            )
            try:
                await album.create()
            except Exception as error:
                logs.debug("Error: %s", error)
                return False
                
        # Artist

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