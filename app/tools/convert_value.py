import hashlib
import mimetypes
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from core.logging import logs

ph = PasswordHasher()

def get_mime(path: str) -> str:
    try:
        type = mimetypes.guess_type(path, strict=True)
        if type:
            return type[0]
        else:
            return 'application/octet-stream'
    except:
        return 'application/octet-stream'


def hash_str(*args) -> str:
    try:
        return hashlib.md5(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''


def safe_list(extra, key, default='') -> str:
    extra = dict(extra)
    
    try:
        value = extra.get(key, [default])
        return value[0] if value else default
    except:
        return ''


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hash: str, password: str) -> tuple[bool, str | None]:
    try:
        ph.verify(hash, password)

        if ph.check_needs_rehash(hash):
            logs.debug("hash_password: needs rehash")
            new_password = ph.hash(password)
            
            return True, new_password
        
        return True, None

    except VerifyMismatchError:
        return False, None
