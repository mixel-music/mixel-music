from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter()

@router.get("/tracks")
async def get_track_list(num: int = Query(500, alias='num', gt=0, le=500)):
    try:
        track_list = await Library.get_tracks(num=num)
        return track_list
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/tracks/{hash}")
async def get_track(hash: str):
    try:
        track_info = await Library.get_tracks(hash)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if track_info:
        return track_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)