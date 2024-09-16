from sqlalchemy import Column, Integer, String, DateTime, Boolean, REAL, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, selectinload

Base = declarative_base()

class Tracks(Base):
    __tablename__ = 'tracks'

    track_id: str = Column(String(32), primary_key=True, nullable=False)
    album_id: str = Column(String(32), ForeignKey('albums.album_id'), nullable=False)
    artist_id: str = Column(String(32), ForeignKey('artists.artist_id'), nullable=False)
    albumartist_id: str = Column(String(32), ForeignKey('albums.albumartist_id'), nullable=False)
    title: str = Column(String, nullable=False)
    album: str = Column(String, nullable=False)
    albumartist: str = Column(String, nullable=False)
    composer: str = Column(String, nullable=False)
    artist: str = Column(String, nullable=False)
    genre: str = Column(String, nullable=False)
    total_track: int = Column(Integer, nullable=False)
    total_disc: int = Column(Integer, nullable=False)
    track: int = Column(Integer, nullable=False)
    disc: int = Column(Integer, nullable=False)
    isrc: str = Column(String, nullable=False)
    label: str = Column(String, nullable=False)
    lyrics: str = Column(String, nullable=False)
    comment: str = Column(String, nullable=False)
    copyright: str = Column(String, nullable=False)
    filepath: str = Column(String, nullable=False)
    filesize: int = Column(Integer, nullable=False)
    duration: float = Column(REAL, nullable=False)
    mime: str = Column(String, nullable=False)
    date: str = Column(String, nullable=False)
    year: int = Column(Integer, nullable=False)
    bitrate: float = Column(REAL, nullable=False)
    bitdepth: int = Column(Integer, nullable=False)
    channels: int = Column(Integer, nullable=False)
    samplerate: int = Column(Integer, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    updated_at: DateTime = Column(DateTime, nullable=False)


class Albums(Base):
    __tablename__ = 'albums'

    album: str = Column(String, nullable=False)
    album_id: str = Column(String(32), primary_key=True, nullable=False)
    albumartist: str = Column(String, ForeignKey('tracks.albumartist'), nullable=False)
    albumartist_id: str = Column(String(32), ForeignKey('artists.artist_id'), nullable=False)
    total_filesize: int = Column(Integer, nullable=False)
    total_duration: float = Column(REAL, nullable=False)
    total_disc: int = Column(Integer, nullable=False)
    year: int = Column(Integer, nullable=False)


class Artists(Base):
    __tablename__ = 'artists'

    artist_id: str = Column(String(32), primary_key=True, nullable=False)
    artist: str = Column(String, nullable=False)


class Artworks(Base):
    __tablename__ = 'artworks'
    
    artwork_id: str = Column(String(32), primary_key=True, nullable=False)
    artwork_type: str = Column(String, nullable=False)
    filepath: str = Column(String, nullable=False)


# class Settings(Base):
#     __tablename__ = 'settings'


class Playlists(Base):
    __tablename__ = 'playlists'

    playlist_id: str = Column(String(32), primary_key=True, nullable=False)
    playlist_name: str = Column(String, nullable=False)
    playlist_user: str = Column(String, ForeignKey('users.user_id'), nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    updated_at: DateTime = Column(DateTime, nullable=False)


class PlaylistsData(Base):
    __tablename__ = 'playlists_data'

    playlist_id: str = Column(String(32), ForeignKey('playlists.playlist_id'), primary_key=True, nullable=False)
    track_id: str = Column(String(32), ForeignKey('tracks.track_id'), nullable=False)
    added_at: DateTime = Column(DateTime, nullable=False)


class Users(Base):
    __tablename__ = 'users'

    user_id: str = Column(String(32), primary_key=True, nullable=False)
    username: str = Column(String, nullable=False)
    nickname: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False)


class UsersData(Base):
    __tablename__ = 'users_data'

    user_id: str = Column(String(32), ForeignKey('users.user_id'), primary_key=True, nullable=False)
    last_login: DateTime = Column(DateTime, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    profile_pic: str = Column(String, nullable=False)
    preferences: str = Column(JSON, nullable=False)


# ---------------------------------------------

# class Tracks(Base):
#     __tablename__ = 'tracks'

#     hash: str = Column(String, primary_key=True, nullable=False)
#     title: str = Column(String, nullable=False)
#     artist: str = Column(String, nullable=False)
#     artisthash: str = Column(String, nullable=False)
#     album: str = Column(String, nullable=False)
#     albumhash: str = Column(String, nullable=False)
#     albumartist: str = Column(String, nullable=False)
#     albumartisthash: str = Column(String, nullable=False)
#     bitdepth: int = Column(Integer, nullable=False)
#     bitrate: float = Column(REAL, nullable=False)
#     channels: int = Column(Integer, nullable=False)
#     comment: str = Column(String, nullable=False)
#     composer: str = Column(String, nullable=False)
#     disc: int = Column(Integer, nullable=False)
#     disctotal: int = Column(Integer, nullable=False)
#     duration: float = Column(REAL, nullable=False)
#     size: int = Column(Integer, nullable=False)
#     genre: str = Column(String, nullable=False)
#     samplerate: int = Column(Integer, nullable=False)
#     track: int = Column(Integer, nullable=False)
#     tracktotal: int = Column(Integer, nullable=False)
#     year: str = Column(String, nullable=False)
#     directory: str = Column(String, nullable=False)
#     mime: str = Column(String, nullable=False)
#     path: str = Column(String, nullable=False)
#     created_date: DateTime = Column(DateTime, nullable=False)
#     updated_date: DateTime = Column(DateTime, nullable=False)
#     unsyncedlyrics: str = Column(String, nullable=False)
#     syncedlyrics: str = Column(String, nullable=False)
#     isrc: str = Column(String(12), nullable=False)


# class Albums(Base):
#     __tablename__ = 'albums'

#     albumhash: str = Column(String, primary_key=True, nullable=False)
#     album: str = Column(String, nullable=False)
#     albumartist: str = Column(String, nullable=False)
#     albumartisthash: str = Column(String, nullable=False)
#     year: str = Column(String, nullable=False)
#     durationtotals: float = Column(REAL, nullable=False)
#     tracktotals: int = Column(Integer, nullable=False) # 이게 꼭 필요할까? 프론트엔드에서 처리해도 될 듯 한데..
#     disctotals: int = Column(Integer, nullable=False)
#     sizetotals: int = Column(Integer, nullable=False)


# class Artists(Base):
#     __tablename__ = 'artists'

#     artisthash: str = Column(String, primary_key=True, nullable=False)
#     artist: str = Column(String, nullable=False)


# from sqlalchemy import (
#     create_engine, Column, String, Integer, ForeignKey, Text, DateTime, Enum, JSON, REAL
# )
# from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy import func
# import enum

# Base = declarative_base()

# class ArtworksType(enum.Enum):
#     albums = "albums"
#     tracks = "tracks"

# class Users(Base):
#     __tablename__ = 'users'
#     user_id = Column(String(32), primary_key=True)
#     username = Column(String, nullable=False, unique=True)
#     nickname = Column(String, nullable=True)
#     password = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     role = Column(String, nullable=False)

# class UsersDetails(Base):
#     __tablename__ = 'users_details'
#     user_id = Column(String(32), ForeignKey('users.user_id'), primary_key=True, nullable=False)
#     last_login = Column(DateTime, default=func.now())
#     created_at = Column(DateTime, default=func.now())
#     profile_picture = Column(String, nullable=True)
#     settings = Column(JSON, nullable=True)

# class Tracks(Base):
#     __tablename__ = 'tracks'
#     track_id = Column(String(32), primary_key=True)
#     album_id = Column(String(32), ForeignKey('albums.album_id'), nullable=True)
#     artist_id = Column(String(32), ForeignKey('artists.artist_id'), nullable=False)
#     file_path = Column(String, nullable=False)
#     file_size = Column(Integer, nullable=False)
#     duration = Column(Integer, nullable=True)
#     bitrate = Column(Integer, nullable=True)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, onupdate=func.now())

# class TracksDetails(Base):
#     __tablename__ = 'tracks_details'
#     track_id = Column(String(32), ForeignKey('tracks.track_id'), primary_key=True, nullable=False)
#     title: str = Column(String, nullable=False)
#     artist: str = Column(String, nullable=False)
#     album: str = Column(String, nullable=False)
#     albumartist: str = Column(String, nullable=False)
#     bitdepth: int = Column(Integer, nullable=False)
#     bitrate: float = Column(REAL, nullable=False)
#     channels: int = Column(Integer, nullable=False)
#     comment: str = Column(String, nullable=False)
#     composer: str = Column(String, nullable=False)
#     disc: int = Column(Integer, nullable=False)
#     disctotal: int = Column(Integer, nullable=False)
#     duration: float = Column(REAL, nullable=False)
#     size: int = Column(Integer, nullable=False)
#     genre: str = Column(String, nullable=False)
#     samplerate: int = Column(Integer, nullable=False)
#     track: int = Column(Integer, nullable=False)
#     tracktotal: int = Column(Integer, nullable=False)
#     year: str = Column(String, nullable=False)
#     mime: str = Column(String, nullable=False)
#     unsyncedlyrics: str = Column(String, nullable=False)
#     syncedlyrics: str = Column(String, nullable=False)
#     isrc: str = Column(String(12), nullable=False)

# class Albums(Base):
#     __tablename__ = 'albums'
#     album_id = Column(String(32), primary_key=True)
#     album_name = Column(String(255), nullable=False)
#     album_artist_id = Column(String(32), ForeignKey('artists.artist_id'), nullable=False)
#     total_discs = Column(Integer, nullable=True)
#     total_lengths = Column(Integer, nullable=True)  # seconds
#     total_sizes = Column(Integer, nullable=True)    # bytes

# class Artists(Base):
#     __tablename__ = 'artists'
#     artist_id = Column(String(32), primary_key=True, nullable=False)
#     artist_name = Column(String(255), nullable=False)
#     artist_description = Column(Text, nullable=True)

# class Artworks(Base):
#     __tablename__ = 'artworks'
#     artwork_id = Column(String(32), primary_key=True, nullable=False)
#     artwork_type = Column(Enum(ArtworksType), nullable=False)
#     related_id = Column(String(32), nullable=False)
#     file_path = Column(String(255), nullable=False)

# class Playlists(Base):
#     __tablename__ = 'playlists'
#     playlist_id = Column(String(32), primary_key=True, nullable=False)
#     user_id = Column(String(32), ForeignKey('users.user_id'), nullable=False)
#     playlist_name = Column(String, nullable=False)
#     created_at = Column(DateTime, default=func.now())

# class PlaylistsTracks(Base):
#     __tablename__ = 'playlists_tracks'
#     playlist_id = Column(String(30), ForeignKey('playlists.playlist_id'), primary_key=True, nullable=False)
#     track_id = Column(String(32), ForeignKey('tracks.track_id'), primary_key=True)
#     added_at = Column(DateTime, default=func.now())


'''
{'filename': WindowsPath(''), 'filesize': int, 'duration': float, 'channels': int, 'bitrate': float, 'bitdepth': int, 'samplerate': int, 'artist': 'ぼっちぼろまる, KMNZ LIZ', 'albumartist': 'ぼっちぼろまる', 'composer': None, 'album': 'BOTCHI BOX vol.1', 'disc': 1, 'disc_total': 1, 'title': 'タンタカタンタンタンタンメン (feat. KMNZ LIZ)', 'track': 1, 'track_total': 6, 'genre': None, 'year': None, 'comment': '', 'extra': {'_year': ['2020'], 'album artist': ['ぼっちぼろまる']}, 'images': {'front_cover': [], 'back_cover': [], 'leaflet': [], 'media': [], 'other': [], 'extra': {}}}
'''