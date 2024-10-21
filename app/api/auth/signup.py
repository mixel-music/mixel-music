from fastapi import Depends, APIRouter
from core.depends import get_user_service
from models.user import UserSignupForm

router = APIRouter()

@router.post('/signup')
async def api_signup(
    form: UserSignupForm,
    service: get_user_service = Depends(),
) -> None:
    
    await service.create_user(form)
