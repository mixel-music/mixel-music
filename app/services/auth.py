import uuid
import diskcache
from typing import Any, Optional
from core.config import Config
from tools.path_handler import get_path


class AuthService:
    session_storage = diskcache.Cache(get_path(Config.DATADIR))
    
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
    def get_username(cls, session_id: Optional[str]) -> tuple[str | Any]:
        if session_id in cls.session_storage:
            return cls.session_storage.get(session_id)
        
        return None
