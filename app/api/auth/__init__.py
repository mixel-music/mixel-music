from fastapi import APIRouter
from .logout import router
from .signin import router
from .signup import router

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

auth_router.include_router(logout.router)
auth_router.include_router(signin.router)
auth_router.include_router(signup.router)