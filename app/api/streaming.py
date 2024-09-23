from fastapi import (
    APIRouter, Header, status, Response, HTTPException, Depends
)
from core.depends import get_service

router = APIRouter(prefix='/api')

@router.get('/streaming/{track_id}', summary="Streaming")
async def api_streaming(
    track_id: str,
    range: str = Header(None),
    service=Depends(get_service)
) -> Response:

    try:
        content, headers = await service.streaming(track_id, range)

        if content:
            return Response(
                content=content,
                headers=headers,
                status_code=status.HTTP_206_PARTIAL_CONTENT
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)