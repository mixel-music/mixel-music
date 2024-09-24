from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select, func, or_, join
from core.database import *
from models import *
from models.album import AlbumItem, AlbumItemResponse, AlbumList
from models.artist import ArtistItem, ArtistItemResponse, ArtistList
from models.track import TrackItem, TrackItemResponse, TrackList


class LibraryRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn


    async def get_track_list(self, page: int, item: int) -> TrackList:
        track_list, total = [], 0
        db_query = await self.conn.execute(
            select(
                Track.album,
                Track.album_id,
                Track.artist,
                Track.artist_id,
                Track.duration,
                Track.title,
                Track.track_id,
            )
            .order_by(Track.title.asc())
            .offset(page)
            .limit(item)
        )
        track_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Track)
        )
        total = total_query.scalar_one()
        return track_list, total
    

    async def get_track_info(self, track_id: str) -> TrackItemResponse:
        track_info = {}
        db_query = await self.conn.execute(
            select(Track.__table__).where(Track.track_id == track_id)
        )
        track_info = dict(db_query.mappings().first())
        return track_info


    async def get_album_list(self, page: int, item: int) -> AlbumList:
        album_list, total = [], 0
        album_query = await self.conn.execute(
            select(
                Album.album,
                Album.album_id,
                Artist.artist.label('albumartist'),
                Album.albumartist_id,
                Album.year,
            )
            .select_from(
                join(
                    Album, Artist,
                    Album.albumartist_id == Artist.artist_id
                )
            )
            .order_by(Album.album.asc())
            .offset(page)
            .limit(item)
        )
        album_list = [dict(row) for row in album_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Album)
        )
        total = total_query.scalar_one()
        return album_list, total
    

    async def get_album_info(self, album_id: str) -> AlbumItemResponse:
        album_info = {}
        album_query = await self.conn.execute(
            select(
                Album.__table__,
                Artist.artist.label('albumartist')
            )
            .select_from(
                join(
                    Album, Artist,
                    Album.albumartist_id == Artist.artist_id
                )
            )
            .where(Album.album_id == album_id)
        )
        album_row = album_query.mappings().first()

        if album_row:
            album_info = dict(album_row)

            # 트랙 정보 가져오기
            track_query = await self.conn.execute(
                select(
                    Track.artist,
                    Track.artist_id,
                    Track.comment,
                    Track.duration,
                    Track.title,
                    Track.track_id,
                    Track.track_number,
                )
                .where(Track.album_id == album_id)
                .order_by(Track.track_number.asc())
            )
            album_info['tracks'] = [dict(row) for row in track_query.mappings().all()]

        return album_info


    async def get_artist_list(self, page: int, item: int) -> ArtistList:
        artist_list, total = [], 0
        db_query = await self.conn.execute(
            select(Artist.__table__).order_by(Artist.artist.asc()).offset(page).limit(item)
        )
        artist_list = [dict(row) for row in db_query.mappings().all()]

        total_query = await self.conn.execute(
            select(func.count()).select_from(Artist)
        )
        total = total_query.scalar_one()

        return artist_list, total


    async def get_artist_info(self, artist_id: str) -> ArtistItemResponse:
        artist_info = {}
        track_query = await self.conn.execute(
            select(Track.album_id)
            .where(or_(Track.artist_id == artist_id, Track.albumartist_id == artist_id))
        )
        tracks_data = track_query.mappings().all()

        if tracks_data:
            # 해당 아이템 있으면 album_id 사용하여 앨범 검색
            album_ids = [track['album_id'] for track in tracks_data]
            album_from_tracks_query = await self.conn.execute(
                select(
                    Album.album,
                    Album.album_id,
                    Album.albumartist_id,
                    Album.year,
                )
                .where(Album.album_id.in_(album_ids))
                .order_by(Album.year.asc())
            )
            
            albums_data = album_from_tracks_query.mappings().all()
            albums_data = [dict(album) for album in albums_data]

            if albums_data:
                album = albums_data[0]
                
                # 앨범 albumartist_id 이용하여 아티스트 조회
                artist_query = await self.conn.execute(
                    select(Artist.artist)
                    .where(Artist.artist_id == album['albumartist_id'])
                )
                artist_data = artist_query.mappings().first()

                if artist_data:
                    artist_info = {
                        'artist': artist_data['artist'],
                        'artist_id': artist_id,
                        'albums': albums_data
                    }

        return artist_info
    

    async def get_scan_info(self):
        result = await self.conn.execute(select(Track.filepath, Track.filesize))
        result = result.all()

        return result
    

    async def get_item_path(self, id: str):
        result = await self.conn.execute(
            select(Track.filepath)
            .where(
                or_(Track.album_id == id, Track.track_id == id)
            )
        )

        data = result.mappings().first()
        return dict(data) if data else {}

    
    async def get_path_by_track_id(self, track_id: str) -> str:
        result = await self.conn.execute(
            select(Track.filepath).where(Track.track_id == track_id)
        )

        row = result.scalars().first()
        return row if row else ''


    async def insert_track(self, track_data: TrackItem) -> None:
        track = Track(**track_data)
        self.conn.add(track)


    async def insert_album(self, album_data: AlbumItem) -> None:
        await self.conn.execute(
            Insert(Album).values(**album_data).on_conflict_do_nothing()
        )


    async def insert_artist(self, artist_data: ArtistItem) -> None:
        await self.conn.execute(
            Insert(Artist).values(**artist_data).on_conflict_do_nothing()
        )


    async def delete_track(self, filepath: str) -> None:
        await self.conn.execute(
            delete(Track).where(Track.filepath == filepath)
        )


    async def delete_album(self, album_id: str) -> None:
        await self.conn.execute(
            delete(Album).where(Album.album_id == album_id)
        )


    async def delete_artist(self, artist_id: str) -> None:
        await self.conn.execute(
            delete(Artist).where(Artist.artist_id == artist_id)
        )