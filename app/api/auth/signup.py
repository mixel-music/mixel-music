from fastapi import Depends, APIRouter
from core.depends import get_user_service
from models.user import UserItem

router = APIRouter()

@router.post('/signup')
async def api_signup(
    user_data: UserItem,
    service: get_user_service = Depends(),
) -> None:
    
    await service.create_user(user_data)
