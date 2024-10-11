from sqlalchemy import Column, Integer, String, REAL
from pydantic import BaseModel
from core.database import Base


class Album(Base):
    __tablename__ = 'albums'

    album: str = Column(String, nullable=False)
    album_id: str = Column(String(32), primary_key=True, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    disc_total: int = Column(Integer, nullable=False)
    duration_total: float = Column(REAL, nullable=False)
    filesize_total: int = Column(Integer, nullable=False)
    year: int = Column(String, nullable=False)


class AlbumList(BaseModel):
    album: str
    album_id: str
    albumartist: str
    albumartist_id: str
    year: int


class AlbumListResponse(BaseModel):
    list: list[AlbumList]
    total: int


class AlbumItem(BaseModel):
    album: str
    album_id: str
    albumartist: str
    albumartist_id: str
    disc_total: int
    duration_total: float
    filesize_total: int
    year: int


class AlbumTrack(BaseModel):
    artist: str
    artist_id: str
    comment: str
    duration: float
    title: str
    track_id: str
    track_number: int


class AlbumItemResponse(AlbumItem):
    tracks: list[AlbumTrack]
