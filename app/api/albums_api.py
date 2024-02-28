from fastapi import APIRouter, status, HTTPException
from core.convert_tools import *
from core.albums_service import *

router = APIRouter()

@router.get("/albums")
async def albums_list_api(num: int = 28) -> list:
    count = sanitize_num(num)
    albums_list = await AlbumsService.list(count)

    return albums_list