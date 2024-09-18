from fastapi import APIRouter, Header, status, Response, HTTPException
from core.library import *

router = APIRouter(prefix = '/api')

@router.get('/streaming/{hash}')
async def api_streaming(hash: str, range: str = Header(None)) -> Response:
    try:
        content, headers = await Library.streaming(hash, range)

        if content:
            return Response(
                content=content,
                headers=headers,
                status_code=status.HTTP_206_PARTIAL_CONTENT
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)