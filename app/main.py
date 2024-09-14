from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncio

from tools.path_handler import create_dir
from api import albums, artists, tracks, artworks, streaming
from core.scanner import find_changes, watch_change
from core.config import Config
from core.database import *
from core.logger import *

@asynccontextmanager
async def init(app: FastAPI):
    create_dir(Config)
    log = log_file_handler()
    await connect_database()
    
    asyncio.create_task(find_changes())
    asyncio.create_task(watch_change())

    try:
        yield
    finally:
        await disconnect_database()
        log.close()

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception) and not isinstance(result, asyncio.CancelledError):
                logs.error(f"Error During Shutdown, {result}")

app = FastAPI(
    debug=Config.DEBUG,
    title=Config.APPNAME,
    version=Config.VERSION,
    lifespan=init,
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
app.include_router(artworks.router)
app.include_router(streaming.router)
app.include_router(tracks.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level=Config.LOGLEVEL,
        log_config=None,
    )