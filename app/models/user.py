from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, JSON, Text, func
)
from pydantic import BaseModel, Field
from core.database import Base

class User(Base):
    __tablename__ = 'users'

    user_id: str = Column(String, primary_key=True, nullable=False)
    username: str = Column(String, nullable=False)
    nickname: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False)


class UserData(Base):
    __tablename__ = 'users_data'

    user_id: str = Column(String, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    last_login: DateTime = Column(DateTime, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    profile_pic: str = Column(String, nullable=False)
    preferences: str = Column(String, nullable=False)