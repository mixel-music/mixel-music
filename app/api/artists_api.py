from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter()

@router.get("/artists")
async def artists_api(num: int = Query(35, alias='num', gt=0, le=100)) -> list:
    artists_list = await Library.get_artists(num=num)

    if not artists_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return artists_list