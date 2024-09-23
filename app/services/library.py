import aiofiles
from core.logging import *
from models.album import AlbumItemResponse, AlbumList
from models.artist import ArtistItemResponse, ArtistList
from models.track import TrackItemResponse, TrackList
from repos.library import *
from tools.path_handler import *


class LibraryService:
    def __init__(self, repo: LibraryRepo) -> None:
        self.repo = repo


    async def get_track_list(self, page: int, item: int) -> TrackList:
        offset = item * (page - 1)
        track_list, total = await self.repo.get_track_list(offset, item)

        return {'list': track_list, 'total': total}


    async def get_track_info(self, track_id: str) -> TrackItemResponse:
        return await self.repo.get_track_info(track_id)


    async def get_album_list(self, page: int, item: int) -> AlbumList:
        offset = item * (page - 1)
        album_list, total = await self.repo.get_album_list(offset, item)

        return {'list': album_list, 'total': total}


    async def get_album_info(self, album_id: str) -> AlbumItemResponse:
        album_info = await self.repo.get_album_info(album_id)
        return album_info


    async def get_artist_list(self, page: int, item: int) -> ArtistList:
        offset = item * (page - 1)
        artist_list, total = await self.repo.get_artist_list(offset, item)

        return {'list': artist_list, 'total': total}


    async def get_artist_info(self, artist_id: str) -> ArtistItemResponse:
        return await self.repo.get_artist_info(artist_id)
    

    async def streaming(self, track_id: str, range: str):
        path = await self.repo.get_path_by_track_id(track_id)
        track_info = await self.repo.get_track_info(track_id)
        if not track_info: return

        track_mime = track_info['content_type']
        track_size = track_info['filesize']
        track_chunk = int(track_size * 0.25)
        real_path = get_path(path)

        if range:
            track_range = range.replace("bytes=", "").split("-")
            track_start = int(track_range[0])
            track_end = int(track_range[1]) if track_range[1] else track_start + track_chunk
        else:
            track_start = 0
            track_end = track_start + track_chunk

        if track_start == 0:
            logs.debug("Playing \"%s\" (%s-%s)", track_info['title'], track_start, track_end)
            
        track_end = min(track_end, track_size - 1)

        async with aiofiles.open(real_path, mode="rb") as track_file:
            await track_file.seek(track_start)
            data = await track_file.read(track_end - track_start + 1)
            headers = {
                'Content-Range': f'bytes {track_start}-{track_end}/{track_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(track_end - track_start + 1),
                'Content-Type': track_mime
            }

            return data, headers