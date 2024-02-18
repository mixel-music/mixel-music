from fastapi import APIRouter, Header, status, Response
from core.tracks import *
from tools.path import *

router = APIRouter()

@router.get("/stream/{id}")
async def api_stream(id: str, range: str = Header(None)):
    music_path = await get_abs_path_from_id(id)
    
    if music_path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    music_info = await TracksObject.get_info(id)
    music_mime = music_info['mime']
    music_size = music_info['size']
    music_chunk = int(music_size * 0.25) # 25% of file size

    if range:
        music_range = range.replace("bytes=", "").split("-")
        music_start = int(music_range[0])
        music_end = int(music_range[1]) if music_range[1] else music_start + music_chunk
    else:
        music_start = 0
        music_end = music_start + music_chunk

    music_end = min(music_end, music_size - 1) # ensure it does not exceed the file size
    logs.debug("Streaming partial data in '%s'...", get_name(music_path)[0])

    async with aiofiles.open(music_path, mode="rb") as music_file:
        await music_file.seek(music_start)
        data = await music_file.read(music_end - music_start + 1)
        headers = {
            'Content-Range': f'bytes {music_start}-{music_end}/{music_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(music_end - music_start + 1),
            'Content-Type': music_mime
        }

        return Response(data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)