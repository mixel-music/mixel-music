from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, JSON, Text, func
)
from pydantic import BaseModel
from core.database import Base


# class Setting(Base):
#     __tablename__ = 'settings'
