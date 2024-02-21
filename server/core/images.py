from mutagen.aiff import AIFF
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.asf import ASF
from model.model import *
from tools.path import *
from core.logs import *
from PIL import Image
import imghdr
import io
import re

IMAGE_QUALITY = 70
IMAGE_SUFFIX = 'webp'
IMAGE_SIZES = [(64, 64), (128, 128), (300, 300)]

class Images:
    def __init__(self, path: str | Path):
        self.path = get_path(path, rel=False)
        self.imgpath = get_path('data', 'images', rel=False)
        self.strpath = get_strpath(self.path)

        if self.path.is_dir():
            logs.error("It's directory.")

        self.id = get_hash(self.strpath)
        self.suffix = get_name(self.strpath)[2]
        self.image_data = None
        
    async def image_extract(self):
        if self.suffix == '.mp3':
            audio = ID3(self.path)
            for tag in audio.values():
                if isinstance(tag, APIC):
                    self.image_data = tag.data 

        elif self.suffix == '.mp4' or self.suffix == '.m4a' or self.suffix == '.aac':
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
            asyncio.create_task(self.image_insert())

    async def image_insert(self):
        if self.image_data != None:
            self.image_hash = hashlib.md5(self.image_data).hexdigest().upper()
            await db.execute(
                tracks.update().values(imageid = self.image_hash).where(tracks.c.path == self.strpath)
            )

            asyncio.create_task(self.image_process())

    async def image_process(self):
        self.image_hash = hashlib.md5(self.image_data).hexdigest().upper()
        image_original = Image.open(io.BytesIO(self.image_data))
        suffix = imghdr.what(io.BytesIO(self.image_data))

        if suffix is None:
            return None
        
        image_original_path = self.imgpath / f"{self.image_hash}_orig.{suffix}"

        if image_original_path.exists():
            logs.debug("Original image already exists.")
        else:
            image_original_name = self.imgpath / f"{self.image_hash}_orig.{suffix}"
            image_original.save(image_original_name.as_posix(), suffix, quality=IMAGE_QUALITY)

        sizes_pattern = '|'.join([f'{width}_{height}' for width, height in IMAGE_SIZES])
        pattern = re.compile(rf'{self.image_hash}_({sizes_pattern})\.{IMAGE_SUFFIX}$')
        missing_sizes = set([f'{width}_{height}' for width, height in IMAGE_SIZES])

        for file in self.imgpath.iterdir():
            if file.is_file() and pattern.search(file.name):
                match = pattern.search(file.name)
                if match:
                    size = match.group(1)
                    if size in missing_sizes:
                        missing_sizes.remove(size)
        if missing_sizes:
            for size in missing_sizes:
                image_thumbnail = image_original.copy()
                image_thumbnail.thumbnail(tuple(int(item) for item in size.split('_'))) #Image.Resampling.LANCZOS)
                image_thumbnail_name = self.imgpath / f"{self.image_hash}_{size}.{IMAGE_SUFFIX}"
                image_thumbnail.save(image_thumbnail_name.as_posix(), "WEBP", quality=IMAGE_QUALITY)
        else:
            logs.debug("All specified sizes were found.")