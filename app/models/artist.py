from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field
from core.database import Base

class Artist(Base):
    __tablename__ = 'artists'

    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)


class ArtistList(BaseModel):
    artist: str = Field(example='아야츠노 유니')
    artist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')


class ArtistListResponse(BaseModel):
    list: list[ArtistList]
    total: int = Field(example=1)


class ArtistItem(BaseModel):
    artist: str = Field(example='아야츠노 유니')
    artist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')


class ArtistAlbum(BaseModel):
    album: str = Field(example="내꺼 하는 법 (How to be mine)")
    album_id: str = Field(example="816f92318525756fa1d95bf9382fbccb")
    albumartist_id: str = Field(example="6eced76df3a9d6f115dc10818f1bd25c")
    year: int = Field(example=2023)


class ArtistItemResponse(ArtistItem):
    albums: list[ArtistAlbum] = Field(
        examples=[
            [
                {
                    "album": "내꺼 하는 법 (How to be mine)",
                    "album_id": "816f92318525756fa1d95bf9382fbccb",
                    "albumartist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "year": 2023,
                },
                {
                    "album": "내꺼 하는 법 (How to be mine) (Aiobahn Remix)",
                    "album_id": "2b119069f9618855cdb835bada8bdcc0",
                    "albumartist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "year": 2024,
                },
                {
                    "album": "SUPADOPA",
                    "album_id": "55b14ff2d7bdf79517decd51eb3316ef",
                    "albumartist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "year": 2024,
                }
            ]
        ]
    )
