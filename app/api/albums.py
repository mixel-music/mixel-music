from fastapi import APIRouter, status, HTTPException, Query
from core.handler import *
from core.schema import *

router = APIRouter()

@router.get("/albums", response_model=AlbumsListResponse)
async def get_album_list(num: int = Query(500, alias='num', gt=1, le=500)):
    try:
        album_list = await Library.get_albums(num=num)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if album_list:
        return album_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@router.get("/albums/{hash}", response_model=AlbumsResponse)
async def get_album(hash: str):
    try:
        album_info = await Library.get_albums(hash)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if album_info:
        return album_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)