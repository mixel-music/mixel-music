from sqlalchemy import Column, String
from pydantic import BaseModel, Field
from core.database import Base


class Artist(Base):
    __tablename__ = 'artists'

    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)


class ArtistList(BaseModel):
    artist: str
    artist_id: str


class ArtistListResponse(BaseModel):
    list: list[ArtistList]
    total: int


class ArtistItem(BaseModel):
    artist: str
    artist_id: str


class ArtistAlbum(BaseModel):
    album: str
    album_id: str
    albumartist_id: str
    year: int


class ArtistItemResponse(ArtistItem):
    albums: list[ArtistAlbum]
