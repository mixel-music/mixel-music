from fastapi import APIRouter
from .albums import router
from .artists import router
from .artworks import router
from .streaming import router
from .tracks import router

library_router = APIRouter(
    prefix='/library',
    tags=['Library'],
)

library_router.include_router(albums.router)
library_router.include_router(artists.router)
library_router.include_router(artworks.router)
library_router.include_router(streaming.router)
library_router.include_router(tracks.router)