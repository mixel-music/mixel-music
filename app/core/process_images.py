from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.aiff import AIFF
from mutagen.asf import ASF
from PIL import Image
import asyncio
import io

from infra.database import *
from infra.init_logger import *
from infra.handle_path import *

IMAGE_QUALITY = 80
IMAGE_SUFFIX = 'webp'
IMAGE_SIZES = [128, 300, 500]

class Images:
    def __init__(self, path: str | Path):
        self.path = get_path(path)
        self.strpath = str_path(path)
        
        self.suffix = get_filename(self.strpath)[2].lower()
        self.id = get_hash_str(self.strpath)

        self.image_path = get_path('config', 'images')
        self.image_data = None
        
    async def extract(self):
        if self.suffix == '.mp3':
            audio = ID3(self.path)
            for tag in audio.values():
                if isinstance(tag, APIC):
                    self.image_data = tag.data 

        elif self.suffix in ['.mp4', '.m4a', '.aac']:
            audio = MP4(self.path)
            covers = audio.get('covr')
            if covers:
                self.image_data = covers[0]

        elif self.suffix == '.flac':
            audio = FLAC(self.path)
            for picture in audio.pictures:
                if picture.type == 3:
                    self.image_data = picture.data

        elif self.suffix == '.alac':
            audio = MP4(self.path)
            covers = audio.tags.get('covr')
            if covers:
                self.image_data = covers[0].data

        elif self.suffix == '.wma':
            audio = ASF(self.path)
            if 'WM/Picture' in audio.asf_tags:
                pictures = audio.asf_tags['WM/Picture']
                if pictures:
                    self.image_data = pictures[0].value.data

        elif self.suffix == '.aiff':
            audio = AIFF(self.path)
            if audio.tags is None:
                pass

            id3 = ID3(self.path)
            for tag in id3.values():
                if isinstance(tag, APIC):
                    self.image_data = tag.data

        if self.image_data:
            asyncio.create_task(self.insert())

    async def insert(self):
        if not self.image_data == None:
            self.image_hash = hashlib.md5(self.image_data).hexdigest().upper()
            await db.execute(
                tracks.update().values(imageid = self.image_hash).where(tracks.c.path == self.strpath)
            )
            asyncio.create_task(self.process())

    async def process(self):
        self.image_hash = hashlib.md5(self.image_data).hexdigest().upper()
        original_image = Image.open(io.BytesIO(self.image_data))
        suffix = original_image.format.lower()

        if suffix is None: return None
        original_image_path = self.image_path / f"{self.image_hash}_orig.{suffix}"

        if original_image_path.exists():
            pass
            # logs.debug("Original image already exists.")
        else:
            original_image_name = self.image_path / f"{self.image_hash}_orig.{suffix}"
            original_image.save(original_image_name.as_posix(), suffix)

        # ------------
            
        create_list = list(IMAGE_SIZES)
        for file in self.image_path.iterdir():
            for size in IMAGE_SIZES:
                if file.is_file() and file.name.endswith(f'{self.image_hash}_{size}.{IMAGE_SUFFIX}'):
                    create_list.remove(size)

        if create_list:
            for size in create_list:
                thumb_image = original_image.copy()
                thumb_image.thumbnail([size, size], Image.Resampling.LANCZOS)
                thumb_image_name = (self.image_path / f"{self.image_hash}_{size}.{IMAGE_SUFFIX}").as_posix()
                thumb_image.save(thumb_image_name, "WEBP", quality=IMAGE_QUALITY)