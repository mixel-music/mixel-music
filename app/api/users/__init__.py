from fastapi import APIRouter
from .users import router

users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

users_router.include_router(users.router)