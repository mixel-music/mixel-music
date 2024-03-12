from api import albums_api, artists_api, images_api, stream_api, tracks_api
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.watcher import *
from infra.logging import *
from infra.session import *
from tools.standard_path import *
import uvicorn
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging()
    await connect_database()
    asyncio.create_task(find_changes())
    asyncio.create_task(watch_change())

    yield
    await disconnect_database()
    stop_logging()

app = FastAPI(
    debug=True,
    title="mixel-music",
    version="0.1.12a",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(albums_api.router, prefix="/api")
app.include_router(artists_api.router, prefix="/api")
app.include_router(images_api.router, prefix="/api")
app.include_router(stream_api.router, prefix="/api")
app.include_router(tracks_api.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=2843,
        log_level="debug",
        log_config=None,
        reload=True,
    )