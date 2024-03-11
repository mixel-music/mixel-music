from fastapi import APIRouter, Header, status, Response, HTTPException
from core.library import *
from tools.convert_values import *

router = APIRouter()

@router.get("/stream/{hash}")
async def stream_api(hash: str, range: str = Header(None)):
    stream_path = await hash_to_track(hash)
    if not stream_path: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    stream_data, headers = await LibraryTasks.stream(stream_path, range)
    if not stream_data: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return Response(stream_data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)