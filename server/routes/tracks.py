from fastapi import APIRouter, Header, status, Response
from model.model_tracks import *
from tools.path import *

router = APIRouter()

@router.get("/tracks")
async def api_tracks_list():
    tracks_list = await Tracks.get_list()

    return tracks_list

@router.get("/tracks/{id}")
async def api_tracks_info(id: str = None):
    tracks_info = await Tracks.get_info(id)

    return tracks_info