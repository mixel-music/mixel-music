from typing import Any
from models import Playlist
from models.playlist import (
    PlaylistModel,
    PlaylistDataModel
)
from core.database import (
    AsyncConnection,
    select,
    insert,
    Insert,
    delete,
    NoResultFound,
    or_,
    join,
    func,
)

class PlaylistRepo:
    def __init__(self, conn: AsyncConnection) -> None:
        self.conn = conn

    
    async def get_playlists(self, start: int, end: int) -> tuple[list[dict[str, Any]], int]:
        pass


    async def get_playlist(self, playlist_id: str) -> dict[str, Any]:
        pass
