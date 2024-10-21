from fastapi import APIRouter, Query, Depends
from models import TrackListResponse, TrackItemResponse
from core.depends import get_library_service

router = APIRouter()

@router.get('/tracks',
    response_model=TrackListResponse,
)
async def api_track_list(
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_library_service = Depends(),
) -> TrackListResponse:
    
    track_list = await service.get_track_list(start, end)
    return track_list


@router.get('/tracks/{track_id}',
    response_model=TrackItemResponse,
)
async def api_track_item(
    track_id: str,
    service: get_library_service = Depends(),
) -> TrackItemResponse:
    
    track_info = await service.get_track_info(track_id)
    return track_info
