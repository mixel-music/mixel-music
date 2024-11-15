from typing import Literal
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get('/ping',
    response_class=PlainTextResponse,
    responses={
        200: {
            "content": {"text/plain": {"example": "pong"}}
        },
    }
)
async def api_get_ping() -> Literal['pong']:
    return 'pong'
