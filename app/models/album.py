from sqlalchemy import Column, Integer, String, REAL
from pydantic import BaseModel, Field, ConfigDict
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
    album: str = Field(example='내꺼 하는 법 (How to be mine)')
    album_id: str = Field(example='816f92318525756fa1d95bf9382fbccb')
    albumartist: str = Field(example='아야츠노 유니')
    albumartist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')
    year: int = Field(example=2023)


class AlbumListResponse(BaseModel):
    list: list[AlbumList]
    total: int = Field(example=1)


class AlbumItem(BaseModel):
    album: str = Field(example='내꺼 하는 법 (How to be mine)')
    album_id: str = Field(example='816f92318525756fa1d95bf9382fbccb')
    albumartist: str = Field(example='아야츠노 유니')
    albumartist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')
    disc_total: int = Field(example=1)
    duration_total: float = Field(example=265.2266666666667)
    filesize_total: int = Field(example=31173874)
    year: int = Field(example=2023)


class AlbumTrack(BaseModel):
    artist: str = Field(example='아야츠노 유니')
    artist_id: str = Field(example='6eced76df3a9d6f115dc10818f1bd25c')
    comment: str = Field(example='')
    duration: float = Field(example=132.61333333333334)
    title: str = Field(example='내꺼 하는 법 (How to Be Mine)')
    track_id: str = Field(example='8c2275ee99b8adfabf88f2e1c937e888')
    track_number: int = Field(example=1)


class AlbumItemResponse(AlbumItem):
    tracks: list[AlbumTrack]
