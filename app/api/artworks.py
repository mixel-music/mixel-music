from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, StreamingResponse

from core.artworks import *
from tools.convert_value import *

import threading
import io

router = APIRouter(prefix = '/api')

@router.get('/artworks/{hash}')
async def api_artworks(hash: str, size: int = Query(300, ge=0)):
    path = await ArtworkService.get_artwork(hash, size)
    if path:
        return FileResponse(path)
    else:
        data = await ArtworkService.init_artwork(hash)
        if data:
            with Image.open(io.BytesIO(data)) as img:
                format = img.format.lower()
                img.thumbnail([size, size], Image.Resampling.LANCZOS)
                io_task = threading.Thread(target=ArtworkService.save_artwork, args=(img, hash, size, format))
                io_task.start()

                buffer = io.BytesIO()
                img.save(buffer, format)
                buffer.seek(0)

                return StreamingResponse(buffer)
        else:
            return None