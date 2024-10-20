import uuid
from typing import Any, Optional
from fastapi import HTTPException, status
from models import UserItem, UserSignup
from repos.user import UserRepo
from tools.convert_value import hash_password, verify_password


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def get_user_info(self, user_id: str) -> None:
        pass


    async def get_user_data(self, user_id: str) -> None:
        pass


    async def get_all_users(self, user_id: str) -> None:
        pass


    async def get_user_count(self) -> int:
        return await self.repo.get_user_count()


    async def update_profile_pic(self, user_id: str) -> None:
        pass


    async def update_preferences(self, user_id: str) -> None:
        pass


    async def check_credential(self, username: str, password: str) -> bool:
        saved_password = await self.repo.get_password(username)
        check_result = verify_password(saved_password, password)

        if not check_result[0]:
            return False
        elif check_result[0] and check_result[1]:
            print("Need rehash")
            return True
        else:
            return True

    
    async def create_user(self, user_data: UserSignup) -> None:
        check_user = await self.repo.is_user_exist(user_data.email)
        if check_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        hashed_password = hash_password(user_data.password)
        user_item = UserItem(
            user_id=str(uuid.uuid4()),
            username=user_data.username,
            password=hashed_password,
            email=user_data.email,
        )
        await self.repo.create_user(user_item.model_dump())


    async def update_user(self, user_data: dict[str, Any]) -> None:
        check_user = await self.repo.is_user_exist(user_data.user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.update_user(user_data)


    async def delete_user(self, user_id: str) -> None:
        check_user = await self.repo.is_user_exist(user_id)
        if not check_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await self.repo.delete_user(user_id)
