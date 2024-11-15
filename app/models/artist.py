from sqlalchemy import Column, String
from pydantic import BaseModel, Field
from core.database import Base


class Artist(Base):
    __tablename__ = 'artists'

    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)


class ArtistModel(BaseModel):
    artist: str
    artist_id: str


class ArtistAlbumModel(BaseModel):
    album: str
    album_id: str
    albumartist_id: str
    year: int


class ArtistsModel(BaseModel):
    artist: str
    artist_id: str


class ArtistResponseModel(ArtistModel):
    albums: list[ArtistAlbumModel]


class ArtistsResponseModel(BaseModel):
    artists: list[ArtistsModel]
    total: int
