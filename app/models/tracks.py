from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, Text, func
from pydantic import BaseModel, Field
from core.database import Base
from datetime import datetime


class Tracks(Base):
    __tablename__ = 'tracks'

    album: str = Column(String, ForeignKey('albums.album'), nullable=False)
    album_id: str = Column(String(32), nullable=False)
    albumartist: str = Column(String, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), nullable=False)
    artwork_id: str = Column(String(32), nullable=False)
    bitdepth: int = Column(Integer, nullable=False)
    bitrate: float = Column(REAL, nullable=False)
    channels: int = Column(Integer, nullable=False)
    compilation: bool = Column(Boolean, nullable=False)
    comment: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    content_type: str = Column(String, nullable=False)
    created_at: DateTime = Column(DateTime, default=func.now())
    date: str = Column(String, nullable=False)
    director: str = Column(String, nullable=False)
    directory: str = Column(String, nullable=False)
    duration: float = Column(REAL, nullable=False)
    disc_number: int = Column(Integer, nullable=False)
    disc_total: int = Column(Integer, nullable=False)
    filepath: str = Column(String, nullable=False)
    filesize: int = Column(Integer, nullable=False)
    genre: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)
    label: str = Column(String, nullable=False)
    lyrics: str = Column(Text, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    title: str = Column(String, nullable=False)
    track_id: str = Column(String(32), primary_key=True, nullable=False)
    track_number: int = Column(Integer, nullable=False)
    track_total: int = Column(Integer, nullable=False)
    updated_at: DateTime = Column(DateTime, onupdate=func.now())
    year: int = Column(Integer, nullable=False)


class TracksList(BaseModel):
    album: str = Field(examples=['내꺼 하는 법 (How to be mine)'])
    album_id: str = Field(examples=['816f92318525756fa1d95bf9382fbccb'])
    artist: str = Field(examples=['아야츠노 유니'])
    artist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])
    duration: float = Field(examples=['132.613333333333'])
    title: str = Field(examples=['내꺼 하는 법 (How to Be Mine)'])
    track_id: str = Field(examples=['8c2275ee99b8adfabf88f2e1c937e888'])


class TracksListResponse(BaseModel):
    list: list[TracksList]
    total: int = Field(examples=['1'])


class TracksItemResponse(BaseModel):
    album: str = Field(examples=['내꺼 하는 법 (How to be mine)'])
    album_id: str = Field(examples=['816f92318525756fa1d95bf9382fbccb'])
    albumartist: str = Field(examples=['아야츠노 유니'])
    albumartist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])
    artist: str = Field(examples=['아야츠노 유니'])
    artist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])
    artwork_id: str = Field(examples=[''])
    bitdepth: int = Field(examples=['16'])
    bitrate: float = Field(examples=['1002.7874924592801'])
    channels: int = Field(examples=['2'])
    compilation: bool = Field(examples=['false'])
    comment: str = Field(examples=[''])
    composer: str = Field(examples=[''])
    content_type: str = Field(examples=['audio/x-flac'])
    created_at: datetime = Field(examples=['2024-01-01T00:00:00.000000'])
    date: str = Field(examples=['2023-07-20'])
    director: str = Field(examples=[''])
    directory: str = Field(examples=[''])
    duration: float = Field(examples=['132.61333333333334'])
    disc_number: int = Field(examples=['1'])
    disc_total: int = Field(examples=['1'])
    filepath: str = Field(examples=[''])
    filesize: int = Field(examples=['16622874'])
    genre: str = Field(examples=[''])
    isrc: str = Field(examples=['ZZA0P2308956'])
    label: str = Field(examples=[''])
    lyrics: str = Field(examples=[''])
    samplerate: int = Field(examples=['44100'])
    title: str = Field(examples=['내꺼 하는 법 (How to Be Mine)'])
    track_id: str = Field(examples=['8c2275ee99b8adfabf88f2e1c937e888'])
    track_number: int = Field(examples=['1'])
    track_total: int = Field(examples=['2'])
    updated_at: datetime = Field(examples=['2024-01-01T00:00:00.000000'])
    year: int = Field(examples=['2023'])