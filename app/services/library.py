import aiofiles
from typing import Any
from fastapi import HTTPException, status
from core.database import NoResultFound
from core.logging import logs
from repos.library import LibraryRepo
from tools.path_handler import get_path


class LibraryService:
    def __init__(self, repo: LibraryRepo) -> None:
        self.repo = repo


    async def get_track_list(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        track_list, total = await self.repo.get_track_list(start, end)
        return {
            "list": track_list,
            "total": total
        }


    async def get_track_info(self, track_id: str) -> dict[str, Any]:
        try:
            return await self.repo.get_track_info(track_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        

    async def get_album_list(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        album_list, total = await self.repo.get_album_list(start, end)
        return {
            "list": album_list,
            "total": total
        }


    async def get_album_info(self, album_id: str) -> dict[str, list[dict[str, Any] | None] | Any]:
        try:
            return await self.repo.get_album_info(album_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    async def get_artist_list(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        artist_list, total = await self.repo.get_artist_list(start, end)
        return {
            "list": artist_list,
            "total": total
        }


    async def get_artist_info(self, artist_id: str) -> dict[str, list[dict[str, Any]] | Any]:
        try:
            return await self.repo.get_artist_info(artist_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

    async def streaming(self, track_id: str, range: str) -> tuple[bytes, dict[str, Any]]:
        try:
            path = await self.repo.get_path_by_track_id(track_id)
            track_info = await self.repo.get_track_info(track_id)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

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
