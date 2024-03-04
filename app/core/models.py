from sqlalchemy import Column, Integer, String, DateTime, Boolean, REAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'
    hash = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    album = Column(String, ForeignKey('albums.albumhash'), nullable=False)
    albumhash = Column(String, nullable=False)
    albumartist = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    artists = Column(String, nullable=False)
    artisthash = Column(String, nullable=False)
    mixartist = Column(String, nullable=False)
    composer = Column(String, nullable=False)
    conductor = Column(String, nullable=False)
    director = Column(String, nullable=False)
    lyricist = Column(String, nullable=False)

    bitrate = Column(Integer, nullable=False)
    channels = Column(Integer, nullable=False)
    duration = Column(REAL, nullable=False)
    samplerate = Column(Integer, nullable=False)
    directory = Column(String, nullable=False)
    mime = Column(String, nullable=False)
    path = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)
    imagehash = Column(String, nullable=False)

    date = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    originaldate = Column(String, nullable=False)
    originalyear = Column(String, nullable=False)
    tracknumber = Column(Integer, nullable=False)
    tracktotals = Column(Integer, nullable=False)
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