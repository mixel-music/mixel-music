from typing import Any
from models import User
from core.database import (
    AsyncConnection, select, insert, update, delete, func
)

class UserRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def is_user_exist(self, email: str) -> bool:
        if not email: return False

        query = await self.conn.execute(
            select(User).where(User.email == email)
        )
        result = query.mappings().first()
        return True if result else False
    

    async def get_password(self, email: str) -> str | None:
        query = await self.conn.execute(
            select(User.password).where(User.email == email)
        )
        result = query.mappings().first()
        return None if result is None else result.get('password')


    async def get_user_info(self) -> None:
        pass


    async def get_user_data(self) -> None:
        pass


    async def get_all_users(self) -> dict[str, Any]:
        users_query = await self.conn.execute(select(User.__table__))
        users = users_query.mappings().all()

        total_query = await self.conn.execute(
            select(func.count()).select_from(User)
        )
        total_query = total_query.scalar_one()
        return users, total_query

    
    async def create_user(self, user_data: dict[str, Any]) -> None:
        await self.conn.execute(
            insert(User).values(**user_data)
        )


    async def update_user(self, user_data: dict[str, Any]) -> None:
        await self.conn.execute(
            update(User).values(**user_data)
        )

    
    async def delete_user(self, user_id: str) -> None:
        await self.conn.execute(
            delete(User).where(User.user_id == user_id)
        )
