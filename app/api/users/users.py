from fastapi import APIRouter, Depends, Response, status
from models.user import UserResponseModel, UsersResponseModel, UserUpdateModel
from core.depends import get_user_service

router = APIRouter()

@router.get('/',
    response_model=UsersResponseModel,
)
async def api_get_users(
    service: get_user_service = Depends(),
) -> UsersResponseModel:
    
    users = await service.get_users()
    return users


@router.get('/{user_id}',
    response_model=UserResponseModel,
)
async def api_get_user(
    user_id: str,
    service: get_user_service = Depends(),
) -> UserResponseModel:
    
    user = await service.get_user(user_id)
    return user


@router.put('/{user_id}')
async def api_update_user(
    user_id: str,
    user_data: UserUpdateModel,
    service: get_user_service = Depends()
) -> None:
    
    await service.update_user(user_id, user_data)
    return


@router.delete('/{user_id}')
async def api_delete_user(
    user_id: str,
    service: get_user_service = Depends()
) -> None:
    
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
