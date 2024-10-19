import uuid
import diskcache
from typing import Any, Optional
from fastapi import HTTPException, status
from core.logging import logs
from repos.user import UserRepo


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    @staticmethod
    async def hash_password(password: str) -> str:
        pass


    async def get_user_info(self, user_id: str):
        pass


    async def get_user_data(self, user_id: str):
        pass


    async def get_all_users(self, user_id: str):
        pass


    async def get_user_count(self):
        return await self.repo.get_user_count()


    async def update_profile_pic(self, user_id: str):
        pass


    async def update_preferences(self, user_id: str):
        pass


    async def check_credential(self, username: str, password: str) -> bool:
        check_result = await self.repo.is_user_match(username, password)
        if not check_result: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    
    async def create_user(self, user_data: dict[str, Any]):
        check_user = await self.repo.is_user_exist(user_data.user_id)
        if check_user: raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
        await self.repo.create_user(user_data)


    async def update_user(self, user_data: dict[str, Any]):
        check_user = await self.repo.is_user_exist(user_data.user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.update_user(user_data)


    async def delete_user(self, user_id: str) -> None:
        check_user = await self.repo.is_user_exist(user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.delete_user(user_id)
