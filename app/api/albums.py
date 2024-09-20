from fastapi import APIRouter, Query
from models.album import AlbumListResponse, AlbumItemResponse
from services.library import *

router = APIRouter(prefix = '/api')

@router.get(
        '/albums',
        summary="Album List",
        response_model=AlbumListResponse)
async def api_album_list(
        page: int=Query(1, ge=1),
        item: int=Query(40, ge=1)) -> AlbumListResponse:
    
    album_list = await Library.get_album_list(page, item)
    return album_list


@router.get(
        '/albums/{id}',
        summary="Album Item",
        response_model=AlbumItemResponse)
async def api_album_item(id: str) -> AlbumItemResponse:
    album_info = await Library.get_album_info(id)
    return album_info