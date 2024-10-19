from fastapi import Depends
from core.database import db_conn, AsyncGenerator
from services.library import LibraryService
from services.user import UserService
from repos.library import LibraryRepo
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
