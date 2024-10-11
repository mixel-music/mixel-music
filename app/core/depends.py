from fastapi import Depends, Request, HTTPException
from typing import Any, AsyncGenerator

from core.database import db_conn
from services.library import LibraryService
from services.user import UserService
from repos.library import LibraryRepo
from services.auth import AuthService
from repos.user import UserRepo


async def get_library_repo() -> AsyncGenerator[LibraryRepo, None]:
    async with db_conn() as conn:
        yield LibraryRepo(conn)


async def get_library_service(
    repo: LibraryRepo = Depends(get_library_repo)
) -> LibraryService:
    return LibraryService(repo)


async def get_user_repo() -> AsyncGenerator[UserRepo, None]:
    async with db_conn() as conn:
        yield UserRepo(conn)


async def get_user_service(
    repo: UserRepo = Depends(get_user_repo)
) -> UserService:
    return UserService(repo)


def get_current_user(request: Request) -> str:
    session_id = request.cookies.get("session")
    if not session_id: raise HTTPException(status_code=401, detail="Unauthorized")

    username = AuthService().get_username(session_id)
    if not username: raise HTTPException(status_code=401, detail="Unauthorized")

    return username
