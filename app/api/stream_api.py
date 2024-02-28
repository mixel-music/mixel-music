from fastapi import APIRouter, Header, status, Response, HTTPException
from core.convert_tools import *
from core.tracks_service import *

router = APIRouter()

@router.get("/stream/{id}")
async def stream_api(id: str, range: str = Header(None)):
    stream_path = await id_to_str_path(id)
    if not stream_path: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        tracks = TracksService(stream_path)
        stream_data, headers = await tracks.stream(range)

        return Response(stream_data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)
    except LookupError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)