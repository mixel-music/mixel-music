from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix='/api')

@router.get("/ping",
    response_class=PlainTextResponse,
    summary="Ping Pong",
    responses={
        200: {
            "content": {"text/plain": {"example": "pong"}}
        },
        500: {}
    }
)
async def api_ping() -> None:
    return 'pong'
