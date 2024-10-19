from fastapi import APIRouter
from .auth import auth_router
from .library import library_router
from .server import server_router

api_router = APIRouter(prefix='/api')
api_router.include_router(auth_router)
api_router.include_router(library_router)
api_router.include_router(server_router)
