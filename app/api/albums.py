from fastapi import APIRouter, Query, Depends
from models.album import AlbumListResponse, AlbumItemResponse
from core.depends import get_library_service, get_current_user

router = APIRouter(prefix='/api')

@router.get(
    '/albums',
    summary="Album List",
    response_model=AlbumListResponse,
)
async def api_album_list(
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    auth: get_current_user = Depends(),
    service: get_library_service = Depends(),
) -> AlbumListResponse:
    
    album_list = await service.get_album_list(start, end)
    return album_list


@router.get(
    '/albums/{album_id}',
    summary="Album Item",
    response_model=AlbumItemResponse,
)
async def api_album_item(
    album_id: str,
    auth: get_current_user = Depends(),
    service: get_library_service = Depends(),
) -> AlbumItemResponse:
    
    album_info = await service.get_album_info(album_id)
    return album_info
