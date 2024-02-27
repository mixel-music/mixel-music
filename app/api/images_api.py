from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse
from core.tracks_service import *
from infra.database import *
from infra.handle_path import *

router = APIRouter()

@router.get("/images/{id}")
async def images_api(id: str, size: int | str = 'orig'):
    image_dir = get_path('config', 'images')
    db_result = await db.fetch_one(tracks.select().with_only_columns([tracks.c.imageid]).where(tracks.c.id == id))
    image_id = db_result.imageid if db_result and db_result.imageid else None

    if image_id is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if size == 'orig':
        for orig_image in image_dir.glob(f"{image_id}_orig*"):
            if orig_image.is_file():
                return FileResponse(orig_image)
    elif int(size) in IMAGE_SIZES:
        thumb_image = image_dir / f"{image_id}_{size}.{IMAGE_SUFFIX}"
        if thumb_image.is_file():
            return FileResponse(thumb_image)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)