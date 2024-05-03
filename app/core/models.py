from sqlalchemy import Column, Integer, String, DateTime, Boolean, REAL, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'

    hash: str = Column(String(40), primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    subtitle: str = Column(String, nullable=False)
    album: str = Column(String, ForeignKey('albums.albumhash'), nullable=False)
    albumhash: str = Column(String(40), nullable=False)
    albumartist: str = Column(String, nullable=False)
    artist: str = Column(String, nullable=False)
    artists: str = Column(String, nullable=False)
    artisthash: str = Column(String(40), nullable=False)
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
    imagehash: str = Column(String(40), nullable=False)
    date: str = Column(String, nullable=False)
    year: int = Column(Integer, nullable=False)
    originaldate: str = Column(String, nullable=False)
    originalyear: str = Column(String, nullable=False)
    tracknumber: int = Column(Integer, nullable=False)
    tracktotals: int = Column(Integer, nullable=False)
    discnumber: int = Column(Integer, nullable=False)
    disctotals: int = Column(Integer, nullable=False)
    compilation: bool = Column(Boolean, nullable=False)
    lyrics: str = Column(String, nullable=False)
    comment: str = Column(String, nullable=False)
    barcode: str = Column(String, nullable=False)
    catalognumber: str = Column(String, nullable=False)
    copyright: str = Column(String, nullable=False)
    genre: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)
    label: str = Column(String, nullable=False)
    media: str = Column(String, nullable=False)
    releasetype: str = Column(String, nullable=False)
    musicbrainz_albumartistid: str = Column(String, nullable=False)
    musicbrainz_albumid: str = Column(String, nullable=False)
    musicbrainz_artistid: str = Column(String, nullable=False)
    musicbrainz_trackid: str = Column(String, nullable=False)



class Albums(Base):
    __tablename__ = 'albums'

    albumhash: str = Column(String(40), primary_key=True, nullable=False)
    album: str = Column(String, nullable=False)
    albumartist: str = Column(String, nullable=False)
    imagehash: str = Column(String(40), nullable=False)
    date: str = Column(String, nullable=False)
    year: int = Column(Integer, nullable=False)
    durationtotals: float = Column(REAL, nullable=False)
    tracktotals: int = Column(Integer, nullable=False)
    disctotals: int = Column(Integer, nullable=False)
    sizetotals: int = Column(Integer, nullable=False)
    musicbrainz_albumartistid: str = Column(String, nullable=False)
    musicbrainz_albumid: str = Column(String, nullable=False)



class Artists(Base):
    __tablename__ = 'artists'

    artisthash: str = Column(String(40), primary_key=True, nullable=False)
    artist: str = Column(String, nullable=False)
    imagehash: str = Column(String(40), nullable=False)



class Users(Base):
    __tablename__ = 'users'
    
    username: str = Column(String, primary_key=True, nullable=False)
    password: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    admin: bool = Column(Boolean, nullable=False)