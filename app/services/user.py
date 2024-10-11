import uuid
import diskcache as dc
from typing import Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from core.logging import *
from repos.user import *
from tools.path_handler import *


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def get_user_info(self):
        pass


    async def get_user_data(self):
        pass


    async def get_all_users(self):
        pass


    async def get_user_count(self):
        return await self.repo.get_user_count()


    async def update_profile_pic(self):
        pass


    async def update_preferences(self):
        pass


    async def check_credential(self, username: str, password: str) -> bool:
        check_result = await self.repo.is_user_match(username, password)
        if not check_result: raise HTTPException(status_code=401)

    
    async def create_user(self, user_data: dict[str, Any]):
        check_user = await self.repo.is_user_exist(user_data.user_id)
        if check_user: raise HTTPException(status_code=400, detail="User already exists")
        await self.repo.create_user(user_data)


    async def update_user(self, user_data: dict[str, Any]):
        check_user = await self.repo.is_user_exist(user_data.user_id)
        if not check_user: raise HTTPException(status_code=400)
        await self.repo.update_user(user_data)


    async def delete_user(self, user_id: str) -> None:
        check_user = await self.repo.is_user_exist(user_id)
        if not check_user: raise HTTPException(status_code=400)
        await self.repo.delete_user(user_id)
