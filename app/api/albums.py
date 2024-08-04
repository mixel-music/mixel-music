from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/albums')
async def api_album_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> dict | list[dict]:
    
    try:
        album_list = await Library.get_album_list(page, item)
        if album_list:
            return album_list
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/albums/{hash}')
async def api_album_info(
    hash: str,
) -> dict | list[dict]:
    
    try:
        album_info = await Library.get_album_info(hash)
        if album_info:
            return album_info
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)