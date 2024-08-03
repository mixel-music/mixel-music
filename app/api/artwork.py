from fastapi import APIRouter, status, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from core.library import *
from tools.convert_value import *

router = APIRouter(prefix='/api')

image_status = {}

@router.get("/artwork/{hash}")
async def get_artwork(bg: BackgroundTasks, hash: str, size: int = 300):
    image_path = await Library.get_cover(hash, size)

    if image_path:
        return FileResponse(image_path)

    bg.add_task(generate_image, hash, size)
    return {"message": "Image is being processed, please try again later."}

async def generate_image(hash: str, size: int) -> None:
    await LibraryTask.create_artwork(hash)
    image_path = await Library.get_cover(hash, size)

    if image_path:
        image_status[hash] = "OK"
    else:
        image_status[hash] = "FAILED"