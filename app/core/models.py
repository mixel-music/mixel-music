from sqlalchemy import Column, Integer, String, DateTime, Boolean, REAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'

    hash: str = Column(String(40), primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    artist: str = Column(String, nullable=False)
    artisthash: str = Column(String(40), nullable=False)
    album: str = Column(String, nullable=False)
    albumhash: str = Column(String(40), nullable=False)
    albumartist: str = Column(String, nullable=False)
    bitdepth: int = Column(Integer, nullable=False)
    bitrate: float = Column(REAL, nullable=False)
    channels: int = Column(Integer, nullable=False)
    comment: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    disc: int = Column(Integer, nullable=False)
    disctotal: int = Column(Integer, nullable=False)
    duration: float = Column(REAL, nullable=False)
    size: int = Column(Integer, nullable=False)
    genre: str = Column(String, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    track: int = Column(Integer, nullable=False)
    tracktotal: int = Column(Integer, nullable=False)
    year: str = Column(String, nullable=False)
    directory: str = Column(String, nullable=False)
    mime: str = Column(String, nullable=False)
    path: str = Column(String, nullable=False)
    created_date: DateTime = Column(DateTime, nullable=False)
    updated_date: DateTime = Column(DateTime, nullable=False)

    # extra: str = Column(String, nullable=False)
    lyrics: str = Column(String, nullable=False)
    # barcode: str = Column(String, nullable=False)
    # copyright: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)
    # label: str = Column(String, nullable=False)
    # musicbrainz_albumartistid: str = Column(String, nullable=False)
    # musicbrainz_albumid: str = Column(String, nullable=False)
    # musicbrainz_artistid: str = Column(String, nullable=False)
    # musicbrainz_trackid: str = Column(String, nullable=False)
    # conductor: str = Column(String, nullable=False)
    # director: str = Column(String, nullable=False)
    # lyricist: str = Column(String, nullable=False)


class Albums(Base):
    __tablename__ = 'albums'

    albumhash: str = Column(String(40), primary_key=True, nullable=False)
    album: str = Column(String, nullable=False)
    albumartist: str = Column(String, nullable=False)
    imagehash: str = Column(String(40), nullable=False)
    year: int = Column(Integer, nullable=False)
    durationtotals: float = Column(REAL)
    tracktotals: int = Column(Integer)
    disctotals: int = Column(Integer)
    sizetotals: int = Column(Integer)
    # musicbrainz_albumartistid: str = Column(String, nullable=False)
    # musicbrainz_albumid: str = Column(String, nullable=False)


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