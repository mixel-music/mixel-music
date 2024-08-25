from fastapi import APIRouter, status
from fastapi.responses import FileResponse, JSONResponse

from core.library import *
from tools.convert_value import *

import threading

router = APIRouter(prefix = '/api')

@router.get('/artwork/{hash}')
async def api_artwork(hash: str, type: int = 300):
    artwork_path = await Library.get_artwork(hash, type)

    if artwork_path:
        return FileResponse(artwork_path)
    else:
        io_task = threading.Thread(target=LibraryTask.create_artwork, args=(hash,))
        io_task.start()

        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={'message': 'extracting...'}
        )