from fastapi import APIRouter, status, HTTPException
from core.services import *
from tools.convert_values import *

router = APIRouter()

@router.get("/albums")
async def albums_list_api(num: int = 28) -> list:
    limit = sanitize_num(num)
    albums = await Library.get_albums(num=limit)
    
    if albums:
        return albums
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)