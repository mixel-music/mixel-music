from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter(prefix='/api')

@router.get("/artists")
async def get_artist_list(num: int = Query(40, alias='num', gt=1, le=128)) -> list:
    try:
        artist_list = await Library.get_artists(num=num)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if artist_list:
        return artist_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)