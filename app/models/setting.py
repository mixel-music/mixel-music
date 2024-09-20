from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, JSON, Text, func
from pydantic import BaseModel, Field
from services.database import Base

# class Setting(Base):
#     __tablename__ = 'settings'