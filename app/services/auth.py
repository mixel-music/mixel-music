import uuid
import diskcache as dc
from typing import Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from core.logging import *
from repos.library import *
from tools.path_handler import *


class AuthService:
    session_storage = dc.Cache()

    def __init__(self) -> None:
        pass


    @classmethod
    def create_session(cls, username: str) -> str:
        session_id = str(uuid.uuid4())
        cls.session_storage.set(
            session_id,
            username,
            expire=60 * 60 * 24 * 28,
        )
        return session_id
    

    @classmethod
    def delete_session(cls, session_id: Optional[str]) -> None:
        if session_id: cls.session_storage.delete(session_id)
    

    @classmethod
    async def get_username(cls, session_id: Optional[str]):
        if session_id in cls.session_storage:
            return cls.session_storage.get(session_id)
        
        return None
