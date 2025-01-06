from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from pydantic import BaseModel
from core.database import Base


class Playlist(Base):
    __tablename__ = 'playlists'

    playlist_id: str = Column(String, primary_key=True, nullable=False)
    playlist_name: str = Column(String, nullable=False)
    playlist_user: str = Column(String, ForeignKey('users.user_id'), nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    updated_at: DateTime = Column(DateTime, nullable=False)


class PlaylistModel(BaseModel):
    playlist_id: str
    playlist_name: str
    playlist_user: str
    created_at: datetime
    updated_at: datetime


class PlaylistData(Base):
    __tablename__ = 'playlists_data'

    playlist_id: str = Column(String, ForeignKey('playlists.playlist_id'), primary_key=True, nullable=False)
    track_id: str = Column(String, ForeignKey('tracks.track_id'), nullable=False)
    added_at: DateTime = Column(DateTime, nullable=False)


class PlaylistDataModel(BaseModel):
    playlist_id: str
    track_id: str
    added_at: datetime


class PlaylistsResponseModel(BaseModel):
    playlists: list[PlaylistModel]
    total: int
