from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from core.library import *
from tools.convert_value import *

import io
import threading
from fastapi.responses import StreamingResponse

router = APIRouter(prefix = '/api')

@router.get('/artwork/{hash}')
async def api_artwork(hash: str, size: int = 300):
    artwork_path = await Library.get_artwork(hash, size)

    if artwork_path:
        return FileResponse(artwork_path)
    elif size:
        arts = await LibraryTask._create_artwork(hash, size)
        if arts:
            with Image.open(io.BytesIO(arts)) as img:
                format = img.format.lower()
                img.thumbnail([size, size], Image.Resampling.LANCZOS)
                io_task = threading.Thread(target=save_artwork, args=(img, hash, size))
                io_task.start()

                buffer = io.BytesIO()
                img.save(buffer, format)
                buffer.seek(0)

                return StreamingResponse(buffer)
            
        else:
            return None