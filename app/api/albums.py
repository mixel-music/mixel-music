from fastapi import APIRouter, Query, Depends
from models.album import AlbumListResponse, AlbumItemResponse
from core.depends import get_service

router = APIRouter(prefix='/api')

@router.get(
    '/albums',
    summary="Album List",
    response_model=AlbumListResponse
)
async def api_album_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
    service=Depends(get_service)
) -> AlbumListResponse:
    
    album_list = await service.get_album_list(page, item)
    return album_list


@router.get(
    '/albums/{album_id}',
    summary="Album Item",
    response_model=AlbumItemResponse
)
async def api_album_item(
    album_id: str,
    service=Depends(get_service)
) -> AlbumItemResponse:
    
    album_info = await service.get_album_info(album_id)
    return album_info