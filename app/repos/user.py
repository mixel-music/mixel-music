from typing import Any
from models import User, UserItem
from core.database import (
    AsyncConnection, select, insert, update, delete, func
)

class UserRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def is_user_exist(self, user_id: str) -> bool:
        query = await self.conn.execute(
            select(User).where(User.user_id == user_id)
        )
        result = query.mappings().first()
        return True if result else False
    

    async def is_user_match(self, username: str, password: str) -> bool:
        query = await self.conn.execute(
            select(User).where(
                (User.username == username) & (User.password == password)
            )
        )
        result = query.mappings().first()
        return True if result else False


    async def get_user_info(self) -> None:
        pass


    async def get_user_data(self) -> None:
        pass


    async def get_all_users(self) -> dict[str, Any]:
        query = await self.conn.execute(select(User.__table__))
        result = query.mappings().first()
        return dict(result or {})


    async def get_user_count(self) -> int:
        query = await self.conn.execute(
            select(func.count()).select_from(User)
        )
        total = query.scalar_one()
        return total

    
    async def create_user(self, user_data: UserItem) -> None:
        await self.conn.execute(
            insert(User).values(**user_data.model_dump())
        )


    async def update_user(self, user_data: UserItem) -> None:
        await self.conn.execute(
            update(User).values(**user_data.model_dump())
        )

    
    async def delete_user(self, user_id: str) -> None:
        await self.conn.execute(
            delete(User).where(User.user_id == user_id)
        )
