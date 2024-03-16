from fastapi import APIRouter, Header, status, Response, HTTPException
from core.handler import *
from core.schema import *

router = APIRouter()

@router.get("/stream/{hash}")
async def api_stream(hash: str, range: str = Header(None)):
    try:
        stream_data, headers = await Library.get_stream(hash, range)
        if stream_data:
            return Response(stream_data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)