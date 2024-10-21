from fastapi import APIRouter, Depends
from models import UserListResponse, UserItemResponse
from core.depends import get_user_service

router = APIRouter()

@router.get('/users',
    response_model=UserListResponse,
)
async def api_user_list(
    service: get_user_service = Depends(),
) -> UserListResponse:
    
    user_list = await service.get_all_users()
    return user_list


@router.get('/users/{user_id}',
    response_model=UserItemResponse,
)
async def api_user_item(
    user_id: str,
    service: get_user_service = Depends(),
) -> UserItemResponse:
    
    pass
