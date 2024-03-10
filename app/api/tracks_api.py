from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter()

@router.get("/tracks")
async def tracks_list_api(num: int = Query(35, alias='num', gt=0, le=100)) -> list:
    tracks_list = await Library.get_tracks(num=num)

    if not tracks_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return tracks_list

@router.get("/tracks/{hash}")
async def tracks_api(hash: str) -> dict:
    tracks_path = await hash_to_track(hash)

    if not tracks_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    tracks_info = await Library.get_tracks(tracks_path)

    if not tracks_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return tracks_info