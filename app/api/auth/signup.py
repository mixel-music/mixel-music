from fastapi import Depends, APIRouter
from core.depends import get_user_service
from models.user import UserSignup

router = APIRouter()

@router.post('/signup')
async def api_signup(
    user_data: UserSignup,
    service: get_user_service = Depends(),
) -> None:
    
    await service.create_user(user_data)
