from fastapi import APIRouter
from .ping import router
from .users import router

server_router = APIRouter(
    prefix='/server',
    tags=['Server'],
)

server_router.include_router(ping.router)
server_router.include_router(users.router)