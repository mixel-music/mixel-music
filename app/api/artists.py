from fastapi import APIRouter, Query, Depends
from models.artist import ArtistListResponse, ArtistItemResponse
from core.depends import get_service

router = APIRouter(prefix='/api')

@router.get(
    '/artists',
    summary="Artist List",
    response_model=ArtistListResponse
)
async def api_artist_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
    service=Depends(get_service)
) -> ArtistListResponse:

    artist_list = await service.get_artist_list(page, item)
    return artist_list


@router.get(
    '/artists/{artist_id}',
    summary="Artist Item",
    response_model=ArtistItemResponse
)
async def api_artist_item(
    artist_id: str,
    service=Depends(get_service)
) -> ArtistItemResponse:
    
    artist_info = await service.get_artist_info(artist_id)
    return artist_info
