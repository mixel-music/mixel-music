from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, REAL, JSON, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'
    album: str = Column(String, ForeignKey('albums.album'), nullable=False)
    album_id: str = Column(String(32), nullable=False)
    albumartist: str = Column(String, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), nullable=False)
    artwork_id: str = Column(String(32), nullable=False)
    bitdepth: int = Column(Integer, nullable=False)
    bitrate: float = Column(REAL, nullable=False)
    channels: int = Column(Integer, nullable=False)
    compilation: bool = Column(Boolean, nullable=False)
    comment: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    content_type: str = Column(String, nullable=False)
    created_at: DateTime = Column(DateTime, default=func.now())
    date: str = Column(String, nullable=False)
    director: str = Column(String, nullable=False)
    directory: str = Column(String, nullable=False)
    duration: float = Column(REAL, nullable=False)
    disc_number: int = Column(Integer, nullable=False)
    disc_total: int = Column(Integer, nullable=False)
    filepath: str = Column(String, nullable=False)
    filesize: int = Column(Integer, nullable=False)
    genre: str = Column(String, nullable=False)
    isrc: str = Column(String(12), nullable=False)
    label: str = Column(String, nullable=False)
    lyrics: str = Column(Text, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    title: str = Column(String, nullable=False)
    track_id: str = Column(String(32), primary_key=True, nullable=False)
    track_number: int = Column(Integer, nullable=False)
    track_total: int = Column(Integer, nullable=False)
    updated_at: DateTime = Column(DateTime, onupdate=func.now())
    year: int = Column(Integer, nullable=False)


class Albums(Base):
    __tablename__ = 'albums'
    album: str = Column(String, nullable=False)
    album_id: str = Column(String(32), primary_key=True, nullable=False)
    albumartist_id: str = Column(String(32), nullable=False)
    disc_total: int = Column(Integer, nullable=False)
    duration_total: float = Column(REAL, nullable=False)
    filesize_total: int = Column(Integer, nullable=False)
    year: str = Column(String, nullable=False)


class Artists(Base):
    __tablename__ = 'artists'
    artist: str = Column(String, nullable=False)
    artist_id: str = Column(String(32), primary_key=True, nullable=False)


# class Artworks(Base):
#     __tablename__ = 'artworks'
    
#     artwork_id: str = Column(String, primary_key=True, nullable=False)
#     artwork_type: str = Column(String, nullable=False)
#     filepath: str = Column(String, nullable=False)


# # class Settings(Base):
# #     __tablename__ = 'settings'


# class Playlists(Base):
#     __tablename__ = 'playlists'

#     playlist_id: str = Column(String, primary_key=True, nullable=False)
#     playlist_name: str = Column(String, nullable=False)
#     playlist_user: str = Column(String, ForeignKey('users.user_id'), nullable=False)
#     created_at: DateTime = Column(DateTime, nullable=False)
#     updated_at: DateTime = Column(DateTime, nullable=False)


# class PlaylistsData(Base):
#     __tablename__ = 'playlists_data'

#     playlist_id: str = Column(String, ForeignKey('playlists.playlist_id'), primary_key=True, nullable=False)
#     track_id: str = Column(String, ForeignKey('new_tracks.track_id'), nullable=False)
#     added_at: DateTime = Column(DateTime, nullable=False)


# class Users(Base):
#     __tablename__ = 'users'

#     user_id: str = Column(String, primary_key=True, nullable=False)
#     username: str = Column(String, nullable=False)
#     nickname: str = Column(String, nullable=False)
#     password: str = Column(String, nullable=False)
#     email: str = Column(String, nullable=False)
#     role: str = Column(String, nullable=False)


# class UsersData(Base):
#     __tablename__ = 'users_data'

#     user_id: str = Column(String, ForeignKey('users.user_id'), primary_key=True, nullable=False)
#     last_login: DateTime = Column(DateTime, nullable=False)
#     created_at: DateTime = Column(DateTime, nullable=False)
#     profile_pic: str = Column(String, nullable=False)
#     preferences: str = Column(String, nullable=False)