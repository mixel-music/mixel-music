from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse
from core.library_handler import *

router = APIRouter()

@router.get("/images/{id}")
async def images_api(id: str, size: int | str = 'orig'):
    image_path = await LibraryHandler.images(await id_to_image_id(id), size)

    if image_path:
        return FileResponse(image_path)
    else:
        image_path = await LibraryHandler.images(id, size)
        if image_path: return FileResponse(image_path)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)