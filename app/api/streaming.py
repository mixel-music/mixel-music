from fastapi import APIRouter, Header, status, Response, Depends
from core.depends import get_library_service, get_current_user

router = APIRouter(prefix='/api')

@router.get('/streaming/{track_id}', summary="Streaming")
async def api_streaming(
    track_id: str,
    range: str = Header(None),
    auth: get_current_user = Depends(),
    service: get_library_service = Depends(),
) -> Response:

    content, headers = await service.streaming(track_id, range)
    return Response(
        content=content,
        headers=headers,
        status_code=status.HTTP_206_PARTIAL_CONTENT
    )
