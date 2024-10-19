from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, Text, func
)
from pydantic import BaseModel, Field
from core.database import Base
from datetime import datetime


class Track(Base):
    __tablename__ = 'tracks'

    album: str = Column(String, ForeignKey('albums.album'), nullable=False)
    album_id: str = Column(String(32), nullable=False)
    albumartist: str = Column(String, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), nullable=False)
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


class TrackList(BaseModel):
    album: str = Field(example='내꺼 하는 법 (How to be mine)')
    album_id: str = Field(example='816f92318525756fa1d95bf9382fbccb')
    artist: str = Field(example='아야츠노 유니')
    artist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')
    duration: float = Field(example=132.613333333333)
    title: str = Field(example='내꺼 하는 법 (How to Be Mine)')
    track_id: str = Field(example='8c2275ee99b8adfabf88f2e1c937e888')


class TrackListResponse(BaseModel):
    list: list[TrackList]
    total: int = Field(example=1)


class TrackItem(BaseModel):
    album: str = Field(example='내꺼 하는 법 (How to be mine)')
    album_id: str = Field(example='816f92318525756fa1d95bf9382fbccb')
    albumartist: str = Field(example='아야츠노 유니')
    albumartist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')
    artist: str = Field(example='아야츠노 유니')
    artist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')
    bitdepth: int = Field(example=16)
    bitrate: float = Field(example=1002.7874924592801)
    channels: int = Field(example=2)
    compilation: bool = Field(example=False)
    comment: str = Field(example='')
    composer: str = Field(example='')
    content_type: str = Field(example='audio/x-flac')
    created_at: datetime = Field(example='2024-01-01T00:00:00.000000')
    date: str = Field(example='2023-07-20')
    director: str = Field(example='')
    directory: str = Field(example='')
    duration: float = Field(example=132.61333333333334)
    disc_number: int = Field(example=1)
    disc_total: int = Field(example=1)
    filepath: str = Field(example='')
    filesize: int = Field(example=16622874)
    genre: str = Field(example='')
    isrc: str = Field(example='ZZA0P2308956')
    label: str = Field(example='')
    lyrics: str = Field(example='')
    samplerate: int = Field(example=44100)
    title: str = Field(example='내꺼 하는 법 (How to Be Mine)')
    track_id: str = Field(example='8c2275ee99b8adfabf88f2e1c937e888')
    track_number: int = Field(example=1)
    track_total: int = Field(example=2)
    updated_at: datetime = Field(example='2024-01-01T00:00:00.000000')
    year: int = Field(example=2023)


class TrackItemResponse(TrackItem):
    pass
