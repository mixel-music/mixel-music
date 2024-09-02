from infra.config import *
from PIL import Image
import io

def save_artwork(data: Image, hash: str, size: int) -> None:
    path = conf.ArtworkDir
    # original = Image.open(io.BytesIO(data))
    suffix = data.format.lower()

    # if suffix:
    #     img = original.copy()

    if not size:
        img_name = str_path(
            get_path(
                path / f'{hash[:2]}' / f'{hash[2:4]}' / f'{hash[4:6]}' / f'original.{suffix}',
                create_dir=True,
            ),
            rel=False,
        )
        data.save(img_name)  

    img_name = str_path(
        get_path(
            path / f'{hash[:2]}' / f'{hash[2:4]}' / f'{hash[4:6]}' / f'{size}.{conf.ArtworkFormat}',
            create_dir=True,
        ),
        rel=False,
    )
    data.save(img_name, conf.ArtworkFormat, quality=conf.ArtworkQuality)