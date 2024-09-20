from fastapi import APIRouter, Query
from models.track import TrackListResponse, TrackItemResponse
from services.library import *

router = APIRouter(prefix = '/api')

@router.get(
        '/tracks',
        summary="Track List",
        response_model=TrackListResponse)
async def api_track_list(
        page: int = Query(1, ge=1),
        item: int = Query(40, ge=1)) -> TrackListResponse:
    
    track_list = await Library.get_track_list(page, item)
    return track_list


@router.get(
        '/tracks/{id}',
        summary="Track Item",
        response_model=TrackItemResponse)
async def api_track_item(id: str) -> TrackItemResponse:
    track_info = await Library.get_track_info(id)
    return track_info