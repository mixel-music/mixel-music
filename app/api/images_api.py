from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse
from core.library_handler import *

router = APIRouter()

@router.get("/images/{id}")
async def images_api(id: str, size: int | str = 'orig'):
    image_path = LibraryHandler.images(await id_to_image_id(id), size)

    if image_path:
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)