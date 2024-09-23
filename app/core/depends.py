from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.library import LibraryService
from repos.library import LibraryRepo

async def get_repo(db: AsyncSession = Depends(get_db)):
    return LibraryRepo(db)

async def get_service(repo: LibraryRepo = Depends(get_repo)):
    return LibraryService(repo)