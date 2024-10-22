from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, REAL, JSON, func
)
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from core.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id: str = Column(String, primary_key=True, nullable=False)
    group: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    last_login: DateTime = Column(DateTime, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    profile_pic: str = Column(String, nullable=False)
    preferences: str = Column(JSON, nullable=False)


class UserGroupEnum(str, Enum):
    admin = 'admin'
    guest = 'guest'
    user = 'user'


class UserList(BaseModel):
    user_id: str
    group: UserGroupEnum = UserGroupEnum.user
    email: EmailStr
    username: str
    last_login: Optional[datetime] = datetime(1970, 1, 1)
    created_at: datetime


class UserListResponse(BaseModel):
    list: list[UserList]
    total: int


class UserItem(BaseModel):
    user_id: str
    group: UserGroupEnum = UserGroupEnum.user
    email: EmailStr
    username: str
    password: str
    last_login: Optional[datetime] = datetime(1970, 1, 1)
    created_at: datetime
    profile_pic: Optional[str] = ''
    preferences: Optional[dict] = {}


class UserItemResponse(BaseModel):
    user_id: str
    group: UserGroupEnum = UserGroupEnum.user
    email: EmailStr
    username: str
    last_login: Optional[datetime] = datetime(1970, 1, 1)
    created_at: datetime
    profile_pic: Optional[str] = ''


class UserSigninForm(BaseModel):
    email: EmailStr
    password: str


class UserSignupForm(BaseModel):
    email: EmailStr
    username: str
    password: str
