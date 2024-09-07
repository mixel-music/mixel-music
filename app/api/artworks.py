from fastapi import APIRouter, Query, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from core.artworks import ArtworkService
from PIL import Image
import asyncio
import io

router = APIRouter(prefix='/api')

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
                
                buffer = io.BytesIO()
                img.save(buffer, format)
                buffer.seek(0)

                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, ArtworkService.save_artwork, img, hash, size, format)

                return StreamingResponse(buffer, media_type=f'image/{format}')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)