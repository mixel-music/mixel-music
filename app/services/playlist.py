from typing import Any
from fastapi import HTTPException, status
from core.database import NoResultFound
from core.logging import logs
from repos.playlist import PlaylistRepo


class PlaylistService:
    def __init__(self, repo: PlaylistRepo) -> None:
        self.repo = repo

    
    async def get_playlists(self, start: int, end: int) -> dict[str, list[dict[str, Any]] | int]:
        playlists, total = await self.repo.get_playlists(start, end)
        return {
            "playlists": playlists,
            "total": total
        }

    
    async def get_playlist(self, playlist_id: str) -> dict[str, Any]:
        try:
            return await self.repo.get_playlist(playlist_id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
