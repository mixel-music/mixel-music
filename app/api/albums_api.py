from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter()

@router.get("/albums")
async def albums_list_api(num: int = Query(35, alias='num', gt=1, le=100)) -> list:
    albums_list = await Library.get_albums(num=num)

    if not albums_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return albums_list