from fastapi import APIRouter, status, HTTPException, Query
from core.handler import *
from core.schema import *

router = APIRouter()

@router.get("/tracks", response_model=TracksListResponse)
async def get_track_list(num: int = Query(500, alias='num', gt=1, le=500)):
    try:
        track_list = await Library.get_tracks(num=num)
        return track_list
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/tracks/{hash}", response_model=TracksResponse)
async def get_track(hash: str):
    try:
        track_info = await Library.get_tracks(hash)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if track_info:
        return track_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)