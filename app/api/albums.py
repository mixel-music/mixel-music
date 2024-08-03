from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter(prefix='/api')

@router.get("/albums")
async def get_album_list(num: int = Query(40, alias='num', gt=0, le=128)) -> dict | list[dict]:
    try:
        album_list = await Library.get_albums(num=num)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if album_list:
        return album_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@router.get("/albums/{hash}")
async def get_album(hash: str) -> dict | list[dict]:
    try:
        album_info = await Library.get_albums(hash)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if album_info:
        return album_info
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)