from fastapi import APIRouter, status, HTTPException, Query
from core.library import *
from core.schema import *

router = APIRouter(prefix='/api')

@router.get("/artists", response_model=list[ArtistListSchema])
async def get_artist_list(num: int = Query(500, alias='num', gt=1, le=500)):
    try:
        artist_list = await Library.get_artists(num=num)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if artist_list:
        return artist_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
# @router.get("/artists/{hash}", response_model=ArtistsResponse)
# async def get_artist(hash: str):
#     try:
#         artist_info = await Library.get_artists(hash)
#     except:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     if artist_info:
#         return artist_info
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)