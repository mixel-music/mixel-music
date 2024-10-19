from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, JSON, Text, func
)
from pydantic import BaseModel, Field
from core.database import Base
from datetime import datetime
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    user_id: str = Column(String, primary_key=True, nullable=False)
    username: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    group: str = Column(String, nullable=False)


class UserData(Base):
    __tablename__ = 'users_data'

    user_id: str = Column(String, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    last_login: DateTime = Column(DateTime, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    profile_pic: str = Column(String, nullable=False)
    preferences: str = Column(String, nullable=False)


class UserItem(BaseModel):
    user_id: str = Field(eaxmple='7f11c509-68c1-42ed-a4f4-449d59652b3a')
    username: str = Field(example='user')
    password: str = Field(example='foobar')
    email: Optional[str] = Field(default='')
    group: Optional[str] = Field(example='normal', default='normal')


class UserDataItem(BaseModel):
    user_id: str = Field(example='7f11c509-68c1-42ed-a4f4-449d59652b3a')
    last_login: datetime = Field(example='2024-01-01T00:00:00.000000')
    created_at: datetime = Field(example='2024-01-01T00:00:00.000000')
    profile_pic: str = Field(example='')
    preferences: str = Field(example='')


class UserSignin(BaseModel):
    username: str = Field(example='user')
    password: str = Field(example='foobar')
