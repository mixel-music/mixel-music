from fastapi import APIRouter, Depends, Response, status
from models.playlist import PlaylistsResponseModel
from core.depends import get_playlist_service

router = APIRouter()

@router.get('/')
async def api_get_playlists(
    service: get_playlist_service = Depends(),
) -> PlaylistsResponseModel:
    
    playlists = await service.get_playlists()
    return playlists


@router.post('/')
async def api_create_playlist(
    service: get_playlist_service = Depends(),
):
    
    users = await service.get_users()
    return users


@router.get('/{playlist_id}')
async def api_get_playlist(

):
    pass


@router.put('/{playlist_id}')
async def api_put_playlist(

):
    pass


@router.delete('/{playlist_id}')
async def api_delete_playlist(

):
    pass

