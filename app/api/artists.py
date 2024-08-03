from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get("/artists")
async def get_artists(p: int = Query(1, ge=1), num: int = Query(40, ge=1)) -> list:
    try:
        artist_list = await Library.get_artists(num=num)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if artist_list:
        return artist_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)