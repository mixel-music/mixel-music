from fastapi import Depends, Response, APIRouter
from core.depends import get_user_service
from models.user import UserSigninModel
from services.auth import AuthService

router = APIRouter()

@router.post("/signin")
async def api_post_signin(
    response: Response,
    form: UserSigninModel,
    service: get_user_service = Depends(),
) -> None:
    
    user_id = await service.check_credential(form.email, form.password)
    session_id = AuthService.create_session(user_id)
    await service.user_login(form.email)

    response.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 28,
    )
