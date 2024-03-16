from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import uvicorn

from api import albums, artists, images, stream, tracks
from core.events import *
from infra.config import *
from infra.database import *
from infra.loggings import *
from tools.path_handler import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_directory()
    await connect_database()
    asyncio.create_task(find_changes())
    asyncio.create_task(watch_change())

    yield
    await disconnect_database()

app = FastAPI(
    debug=conf.FASTAPI_DEBUG,
    title=conf.APP_TITLE,
    version=conf.VERSION,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(albums.router, prefix="/api")
app.include_router(artists.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(stream.router, prefix="/api")
app.include_router(tracks.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=conf.APP_HOST,
        port=conf.APP_PORT,
        log_level=conf.LOG_LEVEL,
        log_config=None,
        reload=conf.FASTAPI_DEBUG,
    )