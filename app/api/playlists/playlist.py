from fastapi import APIRouter, Query, Depends, Response
from models.playlist import PlaylistResponseModel
from core.depends import get_playlist_service

router = APIRouter()

@router.get('/{playlist_id}', response_model=PlaylistResponseModel)
async def api_get_playlist(
    playlist_id: str,
    start: int = Query(1, ge=1),
    end: int = Query(40, ge=1),
    service: get_playlist_service = Depends(),
) -> PlaylistResponseModel:
    
    playlist = await service.get_playlist(playlist_id, start, end)
    return playlist


@router.delete('/{playlist_id}')
async def api_delete_playlist(
    playlist_id: str,
    service: get_playlist_service = Depends(),
) -> None:
    
    await service.delete_playlist(playlist_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/')
async def api_create_playlist(
    service: get_playlist_service = Depends(),
):
    
    users = await service.get_users()
    return users


@router.patch('/{playlist_id}')
async def api_patch_playlist(

):
    pass
