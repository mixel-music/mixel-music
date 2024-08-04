from fastapi import APIRouter
from core.library import *
from infra.loggings import *

router = APIRouter(prefix = '/api')

@router.get('/count')
async def api_count(type: int) -> dict:
    if type == 0:
        count = {
            'count': await Library.get_track_count()
        }
        return count
    
    elif type == 1:
        count = {
            'count': await Library.get_album_count()
        }
        return count
    
    elif type == 2:
        count = {
            'count': await Library.get_artist_count()
        }
        return count