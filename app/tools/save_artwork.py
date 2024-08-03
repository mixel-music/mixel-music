from infra.config import *
from PIL import Image
import io

async def convert_image(image_data: bin, albumhash: str) -> None:
    image_path = conf.IMG_DIR
    original_image = Image.open(io.BytesIO(image_data))
    suffix = original_image.format.lower()

    if suffix is None: return
    # original_image_path = image_path / f"{image_hash}_orig.{suffix}"
    # if not original_image_path.exists():
    #     original_image.save(original_image_path.as_posix(), suffix)
        
    create_list = list(conf.IMG_SIZE)
    for file in image_path.iterdir():
        for size in conf.IMG_SIZE:
            if file.is_file() and file.name.endswith(f'{albumhash}_{size}.{conf.IMG_TYPE}'):
                create_list.remove(size)

    if create_list:
        for size in create_list:
            thumb_image = original_image.copy()
            thumb_image.thumbnail([size, size], Image.Resampling.LANCZOS)
            thumb_image_name = (image_path / f"{albumhash}_{size}.{conf.IMG_TYPE}").as_posix()
            thumb_image.save(thumb_image_name, "webp", quality=conf.IMG_QUAL)