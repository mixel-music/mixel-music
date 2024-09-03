from core.models import *
from core.library import *
from core.schema import Config
from tools.convert_value import *
from tools.path_handler import *
from tools.tags_handler import *
from PIL import Image

class ArtworkService:
    def __init__(self) -> None:
        pass


    @staticmethod
    def convert_hash(hash: str, size: int) -> list[Path, str]:
        if size:
            data = hash_str(f'{hash}_{size}') # 해시를 또 해싱함?
            path = get_path(Config.ARTWORKDIR, f'{data[:2]}', f'{data[2:4]}', f'{data[4:6]}', f'{data[6:8]}.{Config.ARTWORKFORMAT}')
            return path, data
        else:
            path = get_path(Config.ARTWORKDIR, f'{hash[:2]}', f'{hash[2:4]}', f'{hash[4:6]}', f'{hash[6:8]}') # 확장자를 모름
            return path, hash
        

    @staticmethod
    async def get_artwork(hash: str, size: int) -> Path | None:
        if size:
            thumb = ArtworkService.convert_hash(hash, size)[0]
            logs.debug('get_artwork: %s, %s', thumb, thumb.is_file())
            return thumb if thumb.is_file() else None
        else:
            for original in Config.ARTWORKDIR.glob(
                str_path(f'{ArtworkService.convert_hash(hash, size)[0]}.*') # 확장자를 모름
            ):
                return original if original.is_file() else None
            

    @staticmethod
    async def init_artwork(hash: str) -> None:
        try:
            async with session() as conn:
                query = select(Tracks.path).where(
                    or_(Tracks.albumhash == hash, Tracks.hash == hash)
                )

                result = await conn.execute(query)
                data = result.mappings().first()
                if data: data = dict(data)

            artwork = await extract_artwork(data.get('path'))
            return artwork

        except Exception as error:
            logs.error('Error(process_artwork): %s', error)
        

    @staticmethod
    def save_artwork(data: Image, hash: str, size: int, format: str = Config.ARTWORKFORMAT) -> None:
        img_name = get_path(
            str_path(
                ArtworkService.convert_hash(hash, size)[0],
                rel=False,
            ),
            create_dir=True,
        )

        if not size:
            data.save(img_name, format)
        else:
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