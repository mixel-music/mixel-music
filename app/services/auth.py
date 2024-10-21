import uuid
from diskcache import Cache
from typing import Any, Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from core.config import Config


class AuthService:
    dc = Cache(Config.DATADIR)
    ph = PasswordHasher()


    @classmethod
    def pw_encode(cls, password: str) -> str:
        return cls.ph.hash(password)


    @classmethod
    def pw_verify(cls, hash_str: str | None, password: str) -> bool:
        try:
            if not hash_str: return False
            
            cls.ph.verify(hash_str, password)
            return True
        
        except VerifyMismatchError:
            return False


    @classmethod
    def create_session(cls, email: str) -> str:
        session_id = str(uuid.uuid4())
        cls.dc.set(session_id, email, expire=60 * 60 * 24 * 28)
        return session_id
    

    @classmethod
    def delete_session(cls, session_id: Optional[str]) -> None:
        if session_id: cls.dc.delete(session_id)
    

    @classmethod
    def get_user_id(cls, session_id: Optional[str]) -> tuple[str | Any]:
        return cls.dc.get(session_id) if session_id in cls.dc else None
