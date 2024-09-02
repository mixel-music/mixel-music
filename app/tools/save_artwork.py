from infra.config import *
from PIL import Image
import io

async def save_artwork(data: bytes, hash: str, size: int) -> None:
    path = conf.IMG_DIR
    original = Image.open(io.BytesIO(data))
    suffix = original.format.lower()

    if suffix:
        img = original.copy()

        if not size:
            img_name = str_path(
                get_path(
                    path / f'{hash[:2]}' / f'{hash[2:4]}' / f'{hash[4:6]}' / f'original.{suffix}',
                    create_dir=True,
                ),
                rel=False,
            )
            img.save(img_name)
            
        elif size < img.width:
            img.thumbnail([size, size], Image.Resampling.LANCZOS)
            img_name = str_path(
                get_path(
                    path / f'{hash[:2]}' / f'{hash[2:4]}' / f'{hash[4:6]}' / f'{size}.{conf.IMG_TYPE}',
                    create_dir=True,
                ),
                rel=False,
            )
            img.save(img_name, conf.IMG_TYPE, quality=conf.IMG_QUAL)
        else:
            return None
    else:
        return None