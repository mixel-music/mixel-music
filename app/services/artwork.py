from concurrent.futures import ThreadPoolExecutor
import aiofiles
import asyncio
from core.config import Config
from services.library import *
from tools.path_handler import *
from tools.tags_handler import *
from PIL import Image


class ArtworkService:
    def __init__(self, repo: LibraryRepo) -> None:
        self.repo = repo


    @staticmethod
    def convert_hash(id: str, size: int) -> tuple[Path, str]:
        if size:
            path = get_path(Config.ARTWORKDIR, f'{id[:2]}', f'{id[2:4]}', f'{id[4:6]}', f'{size}.{Config.ARTWORKFORMAT}')
            return path
        else:
            path = get_path(f'{id[:2]}', f'{id[2:4]}', f'{id[4:6]}', f'{size}')
            return path
        

    @staticmethod
    async def get_artwork(id: str, size: int) -> Path | None:
        if size:
            thumb = ArtworkService.convert_hash(id, size)
            return thumb if thumb.is_file() else None
        else:
            for original in Config.ARTWORKDIR.glob(
                str_path(ArtworkService.convert_hash(id, size)) + '.*' # 확장자를 모름
            ):
                return original if original.is_file() else None


    async def init_artwork(self, id: str) -> tuple[bytes | None, str] | None:
        try:
            data = await self.repo.get_item_path(id)
            artwork_path = get_path(data.get('filepath')).parent
        except:
            return None

        async def read_artwork_file(filepath) -> bytes:
            async with aiofiles.open(filepath, 'rb') as f:
                return await f.read()

        for fs in artwork_path.iterdir():
            if fs.is_file() \
            and fs.suffix.lower() in Config.ARTWORKTARGETS \
            and not is_excluded_file(fs.name):
                return await read_artwork_file(fs)

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            artwork = await loop.run_in_executor(
                executor,
                extract_artwork,
                data.get('filepath')
            )
        
        return artwork


    def save_artwork(
        self,
        data: Image, 
        id: str, 
        size: int,
        type: str = Config.ARTWORKFORMAT
    ) -> None:
        
        if not size:
            img_name = str_path(
                get_path(
                    ArtworkService.convert_hash(id, size),
                    create_dir=True,
                ),
            rel=False)
            data.save(img_name, format=type)

        else:
            img_name = str_path(
                get_path(
                    ArtworkService.convert_hash(id, size),
                    create_dir=True,
                ),
            rel=False)
            data.save(img_name, quality=Config.ARTWORKQUALITY)


    def delete_artwork(self) -> None:
        pass
