from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from core.library import *
from tools.convert_value import *

import io
from fastapi.responses import StreamingResponse

from async_lru import alru_cache

router = APIRouter(prefix = '/api')

@alru_cache(maxsize=10000000)
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

                buffer = io.BytesIO()
                img.save(buffer, format)
                buffer.seek(0)
                
                return StreamingResponse(buffer)
            
        else:
            return None