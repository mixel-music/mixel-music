from fastapi import Depends, Response, APIRouter
from core.depends import get_user_service
from models.user import UserSigninForm
from services.auth import AuthService

router = APIRouter()

@router.post("/signin")
async def api_signin(
    res: Response,
    form: UserSigninForm,
    service: get_user_service = Depends(),
) -> None:
    
    await service.check_credential(form.email, form.password)
    session_id = AuthService.create_session(form.email)

    res.set_cookie(
        key="session",
        value=session_id,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=60 * 60 * 24 * 28,
    )
