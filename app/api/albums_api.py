from fastapi import APIRouter, status, HTTPException, Query
from core.library import *

router = APIRouter()

@router.get("/albums")
async def albums_list_api(num: int = Query(35, alias='num', gt=1, le=100)) -> list[dict]:
    try:
        albums_list = await LibraryTasks.get_albums(num=num)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err)

    if not albums_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return albums_list