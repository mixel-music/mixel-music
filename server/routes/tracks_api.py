from fastapi import APIRouter, status, HTTPException
from core.tracks import *
from tools.path import *

router = APIRouter()

@router.get("/tracks")
async def tracks_list_api(num: int = 28):
    count = safe_int(num)
    tracks_list = await Tracks.get_list(count)

    return tracks_list

@router.get("/tracks/{id}")
async def tracks_info_api(id: str):
    tracks_info = await Tracks.get_info(id)
    if tracks_info == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return tracks_info