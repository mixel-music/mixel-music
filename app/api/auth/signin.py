from fastapi import Depends, Response, APIRouter, HTTPException, status
from core.depends import get_user_service
from models.user import UserSignin
from services.auth import AuthService

router = APIRouter()

@router.post("/signin")
async def api_signin(
    data: UserSignin,
    response: Response,
    service: get_user_service = Depends(),
) -> None:
    
    check_user = await service.check_credential(data.username, data.password)
    if not check_user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session_id = AuthService.create_session(data.username)

    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=60 * 60 * 24 * 28,
    )
