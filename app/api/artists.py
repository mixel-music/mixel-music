from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/artists')
async def api_artist_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> dict | list[dict]:
    
    try:
        artist_list = await Library.get_artist_list(page, item)
        if artist_list:
            return artist_list
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/artists/{hash}')
async def api_artist_info(
    hash: str,
) -> dict | list[dict]:
    
    try:
        artist_info = await Library.get_artist_info(hash)
        if artist_info:
            return artist_info
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)