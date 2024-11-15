from fastapi import APIRouter

sessions_router = APIRouter(
    prefix='/sessions',
    tags=['Sessions'],
)
