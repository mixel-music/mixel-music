from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter(prefix='/api')

@router.get("/tracks")
async def get_track_list(p: int = Query(1, ge=1), num: int = Query(40, ge=1)) -> list | dict:
    try:
        track_list = await Library.get_tracks(page = (p - 1) * num, num = num)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if track_list:
        return track_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@router.get("/tracks/{hash}")
async def get_track(hash: str) -> tuple[list[dict], dict]:
    try:
        track_info = await Library.get_tracks(hash)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if track_info:
        return track_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)