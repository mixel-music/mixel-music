from fastapi import APIRouter, status, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from core.library import *
from tools.convert_value import *

router = APIRouter(prefix = '/api')

@router.get("/artwork/{hash}")
async def get_artwork(bg: BackgroundTasks, hash: str, size: int = 300):
    artwork_path = await Library.get_artwork(hash, size)

    if artwork_path:
        return FileResponse(artwork_path)

    bg.add_task(gen_artwork, hash, size)
    
    return {'message': 'Extracting...'}

async def gen_artwork(hash: str, size: int) -> None:
    await LibraryTask.create_artwork(hash)
    artwork_path = await Library.get_artwork(hash, size)
    artwork_status = {}

    if artwork_path:
        artwork_status[hash] = ''
    else:
        artwork_status[hash] = 'Failed'