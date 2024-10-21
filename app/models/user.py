from enum import Enum
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, REAL, JSON, func
)
from pydantic import BaseModel, Field, EmailStr
from core.database import Base
from datetime import datetime
from typing import Optional


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
    user_id: str = Field(example='7f11c509-68c1-42ed-a4f4-449d59652b3a')
    group: UserGroupEnum = Field(default=UserGroupEnum.user)
    email: EmailStr = Field()
    username: str = Field()
    last_login: Optional[datetime] = Field(datetime(1970, 1, 1))
    created_at: datetime = Field(example='2024-01-01T00:00:00.000000')
    profile_pic: Optional[str] = Field(default='')


class UserListResponse(BaseModel):
    list: list[UserList]
    total: int = Field(example=1)


class UserItem(BaseModel):
    user_id: str = Field(example='7f11c509-68c1-42ed-a4f4-449d59652b3a')
    group: UserGroupEnum = Field(default=UserGroupEnum.user)
    email: EmailStr = Field()
    username: str = Field()
    password: str = Field()
    last_login: Optional[datetime] = Field(datetime(1970, 1, 1))
    created_at: datetime = Field(example='2024-01-01T00:00:00.000000')
    profile_pic: Optional[str] = Field(default='')
    preferences: Optional[dict] = Field(default={})


class UserItemResponse(BaseModel):
    user_id: str = Field(example='7f11c509-68c1-42ed-a4f4-449d59652b3a')
    group: UserGroupEnum = Field(default=UserGroupEnum.user)
    email: EmailStr = Field()
    username: str = Field()
    last_login: Optional[datetime] = Field(datetime(1970, 1, 1))
    created_at: datetime = Field(example='2024-01-01T00:00:00.000000')
    profile_pic: Optional[str] = Field(default='')


class UserSigninForm(BaseModel):
    email: EmailStr = Field()
    password: str = Field()


class UserSignupForm(BaseModel):
    email: EmailStr = Field()
    username: str = Field()
    password: str = Field()
