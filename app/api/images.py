from fastapi import APIRouter, status, HTTPException
from fastapi.responses import FileResponse

from core.library import *
from tools.convert_value import *

router = APIRouter(prefix='/api')

@router.get("/images/{hash}")
async def get_image(hash: str, size: int = 300):
    image_hash = await hash_to_image(hash)
    image_path = await Library.get_images(image_hash, size)

    if image_path:
        return FileResponse(image_path)
    else:
        image_path = await Library.get_images(hash, size)
        if image_path:
            return FileResponse(image_path)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)