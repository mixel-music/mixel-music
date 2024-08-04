from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from core.library import *
from tools.convert_value import *

router = APIRouter(prefix = '/api')

@router.get('/artwork/{hash}')
async def api_artwork(
    hash: str,
    bg_task: BackgroundTasks,
    type: int = 300,
):

    artwork_path = await Library.get_artwork(hash, type)

    if artwork_path:
        return FileResponse(artwork_path)
    else:
        bg_task.add_task(gen_artwork, hash, type)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={'message': 'extracting...'}
        )
    

async def gen_artwork(
    hash: str,
    type: int,
) -> None:
    
    status = {}

    await LibraryTask.create_artwork(hash)
    artwork_path = await Library.get_artwork(hash, type)
    status[hash] = '' if artwork_path else 'Failed'