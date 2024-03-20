from fastapi import APIRouter, Header, status, Response, HTTPException
from core.library import *
from infra.loggings import *

router = APIRouter(prefix='/api/v1')

@router.get("/stream/{hash}")
async def api_stream(hash: str, range: str = Header(None)):
    try:
        stream_data, headers = await Library.stream(hash, range)
        if stream_data:
            return Response(stream_data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as err:
        logs.error("Failed to streaming, %s", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)