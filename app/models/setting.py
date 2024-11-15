from sqlalchemy import Column, String, JSON
from pydantic import BaseModel
from core.database import Base


class Setting(Base):
    __tablename__ = 'settings'

    key = Column(String, primary_key=True, nullable=False, unique=True)
    value = Column(JSON, nullable=False)
