from sqlalchemy import Column, Integer, String, DateTime, Boolean, REAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'

    hash: str = Column(String, primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    artist: str = Column(String, nullable=False)
    artisthash: str = Column(String, nullable=False)
    album: str = Column(String, nullable=False)
    albumhash: str = Column(String, nullable=False)
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
    unsyncedlyrics: str = Column(String, nullable=False)
    syncedlyrics: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)


class Albums(Base):
    __tablename__ = 'albums'

    albumhash: str = Column(String, primary_key=True, nullable=False)
    album: str = Column(String, nullable=False)
    albumartist: str = Column(String, nullable=False)
    albumartisthash: str = Column(String, nullable=False)
    year: str = Column(String, nullable=False)
    durationtotals: float = Column(REAL, nullable=False)
    tracktotals: int = Column(Integer, nullable=False)
    disctotals: int = Column(Integer, nullable=False)
    sizetotals: int = Column(Integer, nullable=False)


class Artists(Base):
    __tablename__ = 'artists'

    artisthash: str = Column(String, primary_key=True, nullable=False)
    artist: str = Column(String, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    
    username: str = Column(String, primary_key=True, nullable=False)
    password: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    admin: bool = Column(Boolean, nullable=False)