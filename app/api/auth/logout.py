from fastapi import Request, Response, APIRouter, HTTPException, status
from services.auth import AuthService

router = APIRouter()

@router.post('/logout')
async def api_logout(
    request: Request,
    response: Response,
) -> None:
    
    session_id = request.cookies.get('session')

    if session_id:
        AuthService.delete_session(session_id)
        response.delete_cookie(key='session')
        return
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='No active session found'
    )
