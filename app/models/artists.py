from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field
from core.database import Base


class Artists(Base):
    __tablename__ = 'artists'

    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)


class ArtistsList(BaseModel):
    artist: str = Field(examples=['아야츠노 유니'])
    artist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])


class ArtistsListResponse(BaseModel):
    list: list[ArtistsList]
    total: int = Field(examples=['1'])


class ArtistsItemResponse(BaseModel):
    artist: str = Field(examples=['아야츠노 유니'])
    artist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])
    albums: list[dict] = Field(
        examples=[
            [
                {
                    "album": "내꺼 하는 법 (How to be mine)",
                    "album_id": "816f92318525756fa1d95bf9382fbccb",
                    "albumartist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "year": "2023",
                },
                {
                    "album": "내꺼 하는 법 (How to be mine) (Aiobahn Remix)",
                    "album_id": "2b119069f9618855cdb835bada8bdcc0",
                    "albumartist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "year": "2024",
                },
                {
                    "album": "SUPADOPA",
                    "album_id": "55b14ff2d7bdf79517decd51eb3316ef",
                    "albumartist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "year": "2024",
                }
            ]
        ]
    )