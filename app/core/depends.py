from fastapi import Depends
from services.library import LibraryService
from repos.library import LibraryRepo
from core.database import db_conn

async def get_repo():
    async with db_conn() as conn:
        yield LibraryRepo(conn)

async def get_service(repo: LibraryRepo = Depends(get_repo)) -> LibraryService:
    return LibraryService(repo)