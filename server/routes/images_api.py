from fastapi import APIRouter, Header, status, HTTPException
from fastapi.responses import FileResponse
from core.tracks import *
from tools.path import *

router = APIRouter()

@router.get("/images/{id}")
async def images_api(id: str, type: int | str = 'orig'):
    img_dir = get_path('data', 'images', rel=False)
    img_id = await db.fetch_one(tracks.select().with_only_columns([tracks.c.imageid]).where(tracks.c.id == id))
    img_id = img_id['imageid'] if img_id and img_id['imageid'] else None

    if img_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if type == 'orig':
        for img_orig in img_dir.glob(f"{img_id}_orig*"):
            if img_orig.is_file():
                return FileResponse(img_orig)
    else:
        img_size = []
        for img_size_list in IMAGE_SIZES:
            img_size += str(IMAGE_SIZES[0][img_size_list])

        print(img_size)
        #     try:
        #         if int(width) != width:
        #             return "HI"
        #         else:
        #             img_resize = img_dir.joinpath(img_id + '_' + str(width) + '_' + str(width) + '.webp')
        #             return FileResponse(img_resize)
        #     except ValueError:
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)