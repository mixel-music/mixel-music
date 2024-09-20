from sqlalchemy import Column, Integer, String, REAL
from pydantic import BaseModel, Field
from services.database import Base

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
    album: str = Field(examples=['내꺼 하는 법 (How to be mine)'])
    album_id: str = Field(examples=['816f92318525756fa1d95bf9382fbccb'])
    albumartist: str = Field(examples=['아야츠노 유니'])
    albumartist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])
    year: int = Field(examples=[2023])


class AlbumListResponse(BaseModel):
    list: list[AlbumList]
    total: int = Field(examples=[1])


class AlbumItemResponse(BaseModel):
    album: str = Field(examples=['내꺼 하는 법 (How to be mine)'])
    album_id: str = Field(examples=['816f92318525756fa1d95bf9382fbccb'])
    albumartist: str = Field(examples=['아야츠노 유니'])
    albumartist_id: str = Field(examples=['6eced76df3a9d6f115dc10818f1bd25c'])
    disc_total: int = Field(examples=[1])
    duration_total: float = Field(examples=[265.2266666666667])
    filesize_total: int = Field(examples=[31173874])
    year: int = Field(examples=[2023])
    tracks: list[dict] = Field(
        examples=[
            [
                {
                    "artist": "아야츠노 유니",
                    "artist_id": "6eced76df3a9d6f115dc10818f1bd25c",
                    "comment": "",
                    "duration": 132.61333333333334,
                    "title": "내꺼 하는 법 (How to Be Mine)",
                    "track_id": "8c2275ee99b8adfabf88f2e1c937e888",
                    "track_number": 1
                }
            ]
        ]
    )