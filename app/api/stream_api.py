from fastapi import APIRouter, Header, status, Response, HTTPException
from core.services import *
from tools.convert_values import *

router = APIRouter()

@router.get("/stream/{hash}")
async def stream_api(hash: str, range: str = Header(None)):
    stream_path = await hash_to_track(hash)
    if not stream_path: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        stream_data, headers = await Library.stream(stream_path, range)
        return Response(stream_data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)
    except LookupError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)