from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from pydantic import BaseModel, Field
from services.database import Base

class Artwork(Base):
    __tablename__ = 'artworks'
    
    artwork_id: str = Column(String, primary_key=True, nullable=False)
    artwork_type: str = Column(String, nullable=False)
    filepath: str = Column(String, nullable=False)