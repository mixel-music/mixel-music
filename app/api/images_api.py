from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse
from core.library import *

router = APIRouter()

@router.get("/images/{hash}")
async def images_api(hash: str, size: int | str = 'orig'):
    image_hash = await hash_to_image(hash)
    image_path = await Library.images(image_hash, size)

    if image_path:
        return FileResponse(image_path)
    else:
        image_path = await Library.images(hash, size)
        if image_path: return FileResponse(image_path)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)