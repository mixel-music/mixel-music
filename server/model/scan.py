from watchfiles import Change, awatch
from model.database import *
from model.cls_images import *
from model.cls_tracks import *
from tools.path import *

## 시작 시 매뉴얼 스캔 진행

## 디렉터리 제외 모든 파일 이벤트 감지 > str rel path md5 id db 조회
## 없으면 태그 생성 시도 > 에러 미발생시 파일 등록
## 파일 수정 및 삭제도 동일, 수정의 경우 update

target_path = get_path('library', is_rel=False, is_str=False)

class ScanTools:
    @staticmethod
    async def manual_scan():
        logs.info("Starting manual scan...")
        pass

    @staticmethod
    async def folder_scan():
        logs.info("Library observer initiated.")
        pass

    @staticmethod
    async def create_file(file_path: Path):
        music = Tracks(get_path(file_path))
        await music.lookup()

    @staticmethod
    async def modify_file(file_path: Path):
        music = Tracks(get_path(file_path))
        await music.update()

    @staticmethod
    async def delete_file(file_path: Path):
        music = Tracks(get_path(file_path))
        await music.delete()

class S2canTools:
    _target_path = get_path('library', is_rel=False, is_str=False)

    @classmethod
    async def manual_scan(cls):
        logs.debug("Manual scan activated. Scanning...")
        target_file = []
        target_file += list(cls._target_path.glob('**/*'))

        if not target_file:
            query = music.delete()
            await database.execute(query=query)

            return None
        
        for target in target_file:
            music_class = Tracks(get_path(target))
            await music_class.lookup()

        return None

    @classmethod
    async def change_scan(cls):
        logs.debug("Starting...")

        async for changes in awatch(cls._target_path, recursive=True):
            for change_type, path in changes:
                file_path = Path(path)
                if file_path.is_dir() and change_type == Change.deleted:
                    await ScanTools.delete_dir(file_path)
                    continue
                elif change_type == Change.modified:
                    await ScanTools.modify_file(file_path)
                    continue
                elif change_type == Change.added:
                    await ScanTools.create_file(file_path)
                elif change_type == Change.deleted:
                    await ScanTools.delete_file(file_path)

    @staticmethod
    async def create_file(file_path: Path):
        music = Tracks(get_path(file_path))
        await music.lookup()

    @staticmethod
    async def modify_file(file_path: Path):
        music = Tracks(get_path(file_path))
        await music.update()

    @staticmethod
    async def delete_file(file_path: Path):
        music = Tracks(get_path(file_path))
        await music.delete()

    @staticmethod
    async def delete_dir(dir_path: Path):
        diff_path = get_path(dir_path)
        query_image = music.select().with_only_columns([music.c.image_id]).where(music.c.path.like(f'{diff_path}%'))
        result = await database.fetch_one(query_image)

        if not result:
            return None
        
        prefix = result['image_id']
        image_path = get_path('data', 'images', is_rel=False, is_str=False)

        for file in image_path.glob(f"{prefix}*"):
            if file.is_file():
                file.unlink(missing_ok=True)

        query = music.delete().where(music.c.path.like(f'{diff_path}%'))
        await database.execute(query)