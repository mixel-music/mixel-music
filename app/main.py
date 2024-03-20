from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import uvicorn

from api.v1 import albums, artists, images, stream, tracks
from core.watcher import *
from infra.config import *
from infra.database import *
from infra.loggings import *
from tools.path_handler import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    conf.DATA_DIR.mkdir(exist_ok=True)
    conf.IMAGES_DIR.mkdir(exist_ok=True)
    conf.LIBRARY_DIR.mkdir(exist_ok=True)
    
    await connect_database()
    asyncio.create_task(find_changes())
    asyncio.create_task(watch_change())

    yield
    await disconnect_database()

app = FastAPI(
    debug=conf.DEBUG,
    title=conf.TITLE,
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

app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(images.router)
app.include_router(stream.router)
app.include_router(tracks.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=conf.HOST,
        port=conf.PORT,
        log_level=conf.LOG_LEVEL,
        log_config=None,
        reload=conf.DEBUG,
    )