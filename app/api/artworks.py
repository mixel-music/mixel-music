from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.responses import FileResponse, StreamingResponse
from services.artwork import ArtworkService
from core.depends import get_library_repo
from PIL import Image
import asyncio
import io

router = APIRouter(prefix='/api')

@router.get('/artworks/{id}', summary="Artwork")
async def api_artworks(
    id: str,
    size: int = Query(300, ge=0),
    repo: get_library_repo = Depends(),
) -> FileResponse:
    
    service = ArtworkService(repo)

    path = await service.get_artwork(id, size)
    if path:
        return FileResponse(path)
    
    data = await service.init_artwork(id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    loop = asyncio.get_running_loop()
    img = await loop.run_in_executor(service.executor, Image.open, io.BytesIO(data))
    format = img.format.lower()

    await loop.run_in_executor(service.executor, img.thumbnail, [size, size], Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format)
    buffer.seek(0)

    await loop.run_in_executor(service.executor, service.save_artwork, img, id, size, format)
    return StreamingResponse(buffer, media_type=f'image/{format}')
