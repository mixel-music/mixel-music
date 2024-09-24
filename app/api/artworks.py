from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.responses import FileResponse, StreamingResponse
from services.artwork import ArtworkService
from core.depends import get_repo
from PIL import Image
import asyncio
import io

router = APIRouter(prefix='/api')

@router.get('/artworks/{id}', summary="Artwork")
async def api_artworks(
    id: str,
    size: int=Query(300, ge=0),
    repo=Depends(get_repo)
) -> FileResponse:
    
    service = ArtworkService(repo)
    path = await service.get_artwork(id, size)

    if path:
        return FileResponse(path)
    else:
        data = await service.init_artwork(id)
        if data:
            with Image.open(io.BytesIO(data)) as img:
                format = img.format.lower()
                img.thumbnail([size, size], Image.Resampling.LANCZOS)
                
                buffer = io.BytesIO()
                img.save(buffer, format)
                buffer.seek(0)

                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, service.save_artwork, img, id, size, format)

                return StreamingResponse(buffer, media_type=f'image/{format}')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        