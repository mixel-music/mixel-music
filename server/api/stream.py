from ..utils import *

router = APIRouter()

@router.get("/stream/{id}")
async def api_stream(id: str, range: str = Header(None)):
    pass