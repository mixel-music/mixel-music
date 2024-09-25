from fastapi import APIRouter, Query, Depends, HTTPException, status
from models.track import TrackListResponse, TrackItemResponse
from sqlalchemy.exc import NoResultFound
from core.depends import get_service

router = APIRouter(prefix='/api')

@router.get(
    '/tracks',
    summary="Track List",
    response_model=TrackListResponse
)
async def api_track_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
    service: get_service = Depends()
) -> TrackListResponse:
    
    track_list = await service.get_track_list(page, item)
    return track_list


@router.get(
    '/tracks/{track_id}',
    summary="Track Item",
    response_model=TrackItemResponse
)
async def api_track_item(
    track_id: str,
    service: get_service = Depends()
) -> TrackItemResponse:
    
    track_info = await service.get_track_info(track_id)
    return track_info
