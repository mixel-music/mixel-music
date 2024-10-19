from fastapi import APIRouter, Query, Depends
from models.artist import ArtistListResponse, ArtistItemResponse
from core.depends import get_library_service

router = APIRouter()

@router.get('/artists',
    response_model=ArtistListResponse,
)
async def api_artist_list(
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_library_service = Depends(),
) -> ArtistListResponse:

    artist_list = await service.get_artist_list(start, end)
    return artist_list


@router.get('/artists/{artist_id}',
    response_model=ArtistItemResponse,
)
async def api_artist_item(
    artist_id: str,
    service: get_library_service = Depends(),
) -> ArtistItemResponse:
    
    artist_info = await service.get_artist_info(artist_id)
    return artist_info
