from models import *
from core.library import *
from core.config import Config
from tools.convert_value import *
from tools.path_handler import *
from tools.tags_handler import *
from PIL import Image

class ArtworkService:
    def __init__(self) -> None:
        pass


    @staticmethod
    def convert_hash(hash: str, size: int) -> tuple[Path, str]:
        if size:
            path = get_path(Config.ARTWORKDIR, f'{hash[:2]}', f'{hash[2:4]}', f'{hash[4:6]}', f'{size}.{Config.ARTWORKFORMAT}')
            return path
        else:
            path = get_path(f'{hash[:2]}', f'{hash[2:4]}', f'{hash[4:6]}', f'{size}')
            return path
        

    @staticmethod
    async def get_artwork(hash: str, size: int) -> Path | None:
        if size:
            thumb = ArtworkService.convert_hash(hash, size)
            # logs.debug('get_artwork: %s, %s', thumb, thumb.is_file())
            return thumb if thumb.is_file() else None
        else:
            for original in Config.ARTWORKDIR.glob(
                str_path(ArtworkService.convert_hash(hash, size)) + '.*' # 확장자를 모름
            ):
                # logs.debug('get_artwork: %s, %s', original, original.is_file())
                return original if original.is_file() else None


    @staticmethod
    async def init_artwork(hash: str) -> tuple[bytes | None, str] | None:
        try:
            async with session() as conn:
                query = select(Tracks.filepath).where(
                    or_(Tracks.album_id == hash, Tracks.track_id == hash)
                )

                result = await conn.execute(query)
                data = result.mappings().first()
                if data:
                    data = dict(data)
                    artwork_path = get_path(data.get('filepath')).parent

                async def read_artwork_file(file_path) -> bytes:
                    # logs.debug(f'Reading file: {file_path}')
                    async with aiofiles.open(file_path, 'rb') as f:
                        return await f.read()

                for fs in artwork_path.iterdir():
                    # logs.debug(f'Checking file: {fs}')
                    if fs.is_file() and fs.suffix.lower() in Config.ARTWORKTARGETS and not is_hidden_file(fs.name):
                        return await read_artwork_file(fs)

                loop = asyncio.get_running_loop()
                with ThreadPoolExecutor() as executor:
                    artwork = await loop.run_in_executor(executor, extract_artwork, data.get('filepath'))
                
                return artwork

        except Exception as error:
            logs.error('Error(process_artwork): %s', error)
            return None
        

    @staticmethod
    def save_artwork(data: Image, hash: str, size: int, type: str = Config.ARTWORKFORMAT) -> None:
        if not size:
            img_name = str_path(
                get_path(
                    ArtworkService.convert_hash(hash, size),
                    create_dir=True,
                ),
                rel=False,
            )

            data.save(img_name, format=type)
        else:
            img_name = str_path(
                get_path(
                    ArtworkService.convert_hash(hash, size),
                    create_dir=True,
                ),
                rel=False,
            )

            data.save(img_name, quality=Config.ARTWORKQUALITY)


    @staticmethod
    def delete_artwork():
        pass


    # @staticmethod
    # def perform_artwork() -> None:
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)

    #     loop.run_until_complete(LibraryTask._perform_artwork())
    #     loop.close()

    
    # @staticmethod
    # async def _perform_artwork() -> None:
    #     try:
    #         async with session() as conn:
    #             db_query = select(Tracks.path, Tracks.album, Tracks.hash)
    #             db_result = await conn.execute(db_query)
    #             result = db_result.mappings().all()

    #     except Exception as error:
    #         logs.error('error %s', error)

    #     for row in result:
    #         if row.album != 'Unknown Album':
    #             check = await Library.get_artwork(hash_str(row.album), 0)
    #             if not check:
    #                 artwork = await extract_artwork(row.path)
    #                 if artwork: asyncio.create_task(save_artwork(artwork, hash_str(row.album), 0))
    #         else:
    #             check = await Library.get_artwork(row.hash, 0)
    #             if not check:
    #                 artwork = await extract_artwork(row.path)
    #                 if artwork: asyncio.create_task(save_artwork(artwork, row.hash, 0))