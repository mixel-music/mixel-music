from sqlalchemy import Column, String, REAL, Integer
from pydantic import BaseModel, Field
from core.database import Base


class Artist(Base):
    __tablename__ = 'artists'

    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)
    album_total: float = Column(Integer, nullable=False)
    track_total: int = Column(Integer, nullable=False)
    duration_total: float = Column(REAL, nullable=False)
    filesize_total: int = Column(Integer, nullable=False)


class ArtistModel(BaseModel):
    artist: str
    artist_id: str
    album_total: int
    track_total: int
    duration_total: float
    filesize_total: int


class ArtistAlbumModel(BaseModel):
    album: str
    album_id: str
    albumartist_id: str
    year: int


class ArtistsModel(BaseModel):
    artist: str
    artist_id: str
    album_total: int
    track_total: int
    duration_total: float
    filesize_total: int


class ArtistResponseModel(ArtistModel):
    albums: list[ArtistAlbumModel]


class ArtistsResponseModel(BaseModel):
    artists: list[ArtistsModel]
    total: int
