from sqlalchemy import Column, Integer, String, DateTime, Boolean, REAL, ForeignKey
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'

    hash: str = Column(String, primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    subtitle: str = Column(String, nullable=False)
    album: str = Column(String, ForeignKey('albums.albumhash'), nullable=False)
    albumhash: str = Column(String, nullable=False)
    albumartist: str = Column(String, nullable=False)
    artist: str = Column(String, nullable=False)
    artists: str = Column(String, nullable=False)
    artisthash: str = Column(String, nullable=False)
    mixartist: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    conductor: str = Column(String, nullable=False)
    director: str = Column(String, nullable=False)
    lyricist: str = Column(String, nullable=False)
    bitrate: int = Column(Integer, nullable=False)
    channels: int = Column(Integer, nullable=False)
    duration: float = Column(REAL, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    directory: str = Column(String, nullable=False)
    mime: str = Column(String, nullable=False)
    path: str = Column(String, nullable=False)
    size: int = Column(Integer, nullable=False)
    created_date: DateTime = Column(DateTime, nullable=False)
    updated_date: DateTime = Column(DateTime, nullable=False)
    imagehash: str = Column(String, nullable=False)
    date: str = Column(String, nullable=False)
    year: int = Column(Integer, nullable=False)
    originaldate: str = Column(String, nullable=False)
    originalyear: str = Column(String, nullable=False)
    tracknumber: int = Column(Integer, nullable=False)
    tracktotals: int = Column(Integer, nullable=False)
    discnumber = Column(Integer, nullable=False)
    disctotals = Column(Integer, nullable=False)
    compilation = Column(Boolean, nullable=False)
    lyrics = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    catalognumber = Column(String, nullable=False)
    copyright = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    isrc = Column(String, nullable=False)
    label = Column(String, nullable=False)
    media = Column(String, nullable=False)
    releasetype = Column(String, nullable=False)
    musicbrainz_albumartistid = Column(String, nullable=False)
    musicbrainz_albumid = Column(String, nullable=False)
    musicbrainz_artistid = Column(String, nullable=False)
    musicbrainz_trackid = Column(String, nullable=False)


class Albums(Base):
    __tablename__ = 'albums'

    albumhash = Column(String, primary_key=True, nullable=False)
    album = Column(String, nullable=False)
    albumartist = Column(String, nullable=False)
    imagehash = Column(String, nullable=False)
    date = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    durationtotals = Column(REAL, nullable=False)
    tracktotals = Column(Integer, nullable=False)
    disctotals = Column(Integer, nullable=False)
    sizetotals = Column(Integer, nullable=False)
    musicbrainz_albumartistid = Column(String, nullable=False)
    musicbrainz_albumid = Column(String, nullable=False)


class Artists(Base):
    __tablename__ = 'artists'

    artisthash = Column(String, primary_key=True, nullable=False)
    artist = Column(String, nullable=False)
    imagehash = Column(Integer, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    
    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)