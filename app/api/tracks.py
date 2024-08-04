from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/tracks')
async def api_track_list(
    page: int = Query(1, ge=1),
    item: int = Query(40, ge=1),
) -> dict | list[dict]:
    
    try:
        track_list = await Library.get_track_list(page, item)
        if track_list:
            return track_list
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/tracks/{hash}')
async def api_track_info(
    hash: str,
) -> dict | list[dict]:
    
    try:
        track_info = await Library.get_track_info(hash)
        if track_info:
            return track_info
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as error:
        logs.error(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)