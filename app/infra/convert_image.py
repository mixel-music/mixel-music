from PIL import Image
from infra.path_handler import *
from infra.setup_logger import *
# import pillow_avif
import hashlib
import io

IMAGE_QUALITY = 100
IMAGE_SUFFIX = 'webp'
IMAGE_SIZES = [128, 300, 500]

async def convert_image(image_data: bin):
    image_path = images_dir()
    image_hash = hashlib.md5(image_data).hexdigest().upper()
    original_image = Image.open(io.BytesIO(image_data))
    suffix = original_image.format.lower()

    if suffix is None: return None
    original_image_path = image_path / f"{image_hash}_orig.{suffix}"

    # if not original_image_path.exists():
    #     original_image.save(original_image_path.as_posix(), suffix)
        
    create_list = list(IMAGE_SIZES)
    for file in image_path.iterdir():
        for size in IMAGE_SIZES:
            if file.is_file() and file.name.endswith(f'{image_hash}_{size}.{IMAGE_SUFFIX}'):
                create_list.remove(size)

    if create_list:
        for size in create_list:
            thumb_image = original_image.copy()
            thumb_image.thumbnail([size, size], Image.Resampling.LANCZOS)
            thumb_image_name = (image_path / f"{image_hash}_{size}.{IMAGE_SUFFIX}").as_posix()
            thumb_image.save(thumb_image_name, "webp", quality=IMAGE_QUALITY)