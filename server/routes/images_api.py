from fastapi import APIRouter, Header, status, HTTPException
from fastapi.responses import FileResponse
from core.tracks import *
from tools.path import *

router = APIRouter()

@router.get("/images/{id}")
async def images_api(id: str, size: int | str = 'orig'):
    img_dir = get_path('data', 'images', rel=False)
    img_id = await db.fetch_one(tracks.select().with_only_columns([tracks.c.imageid]).where(tracks.c.id == id))
    img_id = img_id['imageid'] if img_id and img_id['imageid'] else None

    if img_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if size == 'orig' or int(size) in IMAGE_SIZES:
        for all_images in img_dir.glob(f"{img_id}_{size}.*"):
            if all_images.is_file():
                return FileResponse(all_images)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)