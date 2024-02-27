from fastapi import APIRouter, status, HTTPException
from core.convert_data import *
from core.tracks_service import *

router = APIRouter()

@router.get("/tracks")
async def tracks_list_api(num: int = 28) -> list:
    count = sanitize_num(num)
    tracks_list = await TracksService.list(count)

    return tracks_list

@router.get("/tracks/{id}")
async def tracks_info_api(id: str) -> dict:
    tracks_path = await id_to_str_path(id)
    tracks_info = await TracksService.info(tracks_path)

    if not tracks_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return tracks_info