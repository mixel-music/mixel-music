from fastapi import APIRouter, Header, status, Response
from core.tracks import *
from tools.path import *

router = APIRouter()

@router.get("/tracks")
async def api_tracks_list():
    tracks_list = await TracksObject.get_list()

    return tracks_list

@router.get("/tracks/{id}")
async def api_tracks_info(id: str = None):
    tracks_info = await TracksObject.get_info(id)

    return tracks_info