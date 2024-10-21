import uuid
from datetime import datetime
from typing import Any
from fastapi import HTTPException, status
from models import UserItem, UserSignupForm
from repos.user import UserRepo
from services.auth import AuthService


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def get_user_info(self, user_id: str) -> None:
        pass


    async def get_user_data(self, user_id: str) -> None:
        pass


    async def get_all_users(self) -> dict[str, list[dict[str, Any]] | int]:
        user_list, total = await self.repo.get_all_users()
        return {
            "list": user_list,
            "total": total
        }


    async def update_profile_pic(self, user_id: str) -> None:
        pass


    async def update_preferences(self, user_id: str) -> None:
        pass


    async def check_credential(self, email: str, password: str) -> None:
        if not AuthService.pw_verify(await self.repo.get_password(email), password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    
    async def create_user(self, data: UserSignupForm) -> None:
        check_user = await self.repo.is_user_exist(data.email)
        if check_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        user_item = UserItem(
            user_id=str(uuid.uuid4()),
            email=data.email,
            username=data.username,
            password=AuthService.pw_encode(data.password),
            created_at=datetime.now(),
        )

        await self.repo.create_user(user_item.model_dump())


    async def update_user(self, data: dict[str, Any]) -> None:
        check_user = await self.repo.is_user_exist(data.user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.update_user(data)


    async def delete_user(self, user_id: str) -> None:
        check_user = await self.repo.is_user_exist(user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.delete_user(user_id)
