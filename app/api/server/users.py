from fastapi import APIRouter, Depends
from models.user import UserListResponse, UserItemResponse
from core.depends import get_user_service

router = APIRouter()

@router.get('/users',
    response_model=UserListResponse,
)
async def api_get_user_list(
    service: get_user_service = Depends(),
) -> UserListResponse:
    
    user_list = await service.get_user_list()
    return user_list


@router.get('/users/{user_id}',
    response_model=UserItemResponse,
)
async def api_get_user_item(
    user_id: str,
    service: get_user_service = Depends(),
) -> UserItemResponse:
    
    user_item = await service.get_user_item(user_id)
    return user_item


@router.delete('/users/{user_id}')
async def api_delete_user_item(
    user_id: str,
    service: get_user_service = Depends()
) -> None:
    
    await service.delete_user(user_id)
    return
