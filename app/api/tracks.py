from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from core.schema import *

router = APIRouter()

@router.get("/tracks", response_model=list[TrackListSchema])
async def get_track_list(num: int = Query(500, alias='num', gt=0, le=500)):
    try:
        track_list = await Library.get_tracks(num=num)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if track_list:
        return track_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@router.get("/tracks/{hash}", response_model=TrackSchema)
async def get_track(hash: str):
    try:
        track_info = await Library.get_tracks(hash)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if track_info:
        return track_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)