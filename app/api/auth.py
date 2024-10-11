from fastapi import Depends, Request, Response, APIRouter, HTTPException
from models.user import UserItem, UserSignin
from core.depends import get_user_service
from services.auth import AuthService

router = APIRouter(prefix='/api')

@router.post("/signup", summary="Signup")
async def api_signup(
    user_data: UserItem,
    service: get_user_service = Depends(),
) -> None:
    
    await service.create_user(user_data)


@router.post("/signin", summary="Signin")
async def api_signin(
    data: UserSignin,
    response: Response,
    service: get_user_service = Depends(),
) -> None:
    
    await service.check_credential(data.username, data.password)
    session_id = AuthService().create_session(data.username)
    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24 * 28
    )


@router.post("/logout", summary="Logout")
async def api_logout(
    request: Request,
    response: Response,
) -> None:
    
    session_id = request.cookies.get("session")
    if session_id:
        AuthService().delete_session(session_id)
        response.delete_cookie(key="session")
        return
    
    raise HTTPException(status_code=400, detail="No active session found")
