from fastapi import APIRouter, Query
from models.artist import ArtistListResponse, ArtistItemResponse
from services.library import *

router = APIRouter(prefix = '/api')

@router.get(
        '/artists',
        summary="Artist List",
        response_model=ArtistListResponse)
async def api_artist_list(
        page: int=Query(1, ge=1),
        item: int=Query(40, ge=1)) -> ArtistListResponse:

    artist_list = await Library.get_artist_list(page, item)
    return artist_list


@router.get(
        '/artists/{id}',
        summary="Artist Item",
        response_model=ArtistItemResponse)
async def api_artist_item(id: str) -> ArtistItemResponse:
    artist_info = await Library.get_artist_info(id)
    return artist_info