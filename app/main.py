from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import uvicorn

from api import albums, artists, images, stream, tracks
from core.watcher import *
from infra.config import *
from infra.database import *
from infra.loggings import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    console = init_logger()
    
    conf.TASK_DIR.mkdir(exist_ok=True)
    conf.IMAGE_DIR.mkdir(exist_ok=True)
    conf.MUSIC_DIR.mkdir(exist_ok=True)
    
    await connect_database()
    asyncio.create_task(find_changes())
    asyncio.create_task(watch_change())

    yield
    await disconnect_database()
    console.save_text(conf.LOG_PATH)

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
        reload=conf.DEBUG,
        log_level=conf.LOG_LEVEL,
        log_config=None,
    )