from fastapi import APIRouter, status, HTTPException
from core.library import *
from tools.convert_values import *

router = APIRouter()

@router.get("/artists")
async def artists_list_api(num: int = 35) -> list:
    limit = sanitize_num(num)
    artists = await Library.get_artists(num=limit)
    
    if not artists: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return artists