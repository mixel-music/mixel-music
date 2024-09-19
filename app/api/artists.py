from fastapi import APIRouter, Query
from models.artists import ArtistsListResponse, ArtistsItemResponse
from core.library import *

router = APIRouter(prefix = '/api')

@router.get('/artists')
async def api_artist_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> ArtistsListResponse:

    artist_list = await Library.get_artist_list(page, item)
    return artist_list


@router.get('/artists/{hash}')
async def api_artist_info(
    hash: str,
) -> ArtistsItemResponse:

    artist_info = await Library.get_artist_info(hash)
    return artist_info