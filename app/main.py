from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api import images_api, stream_api, tracks_api
from core.event_watcher import *
from infra.database import *
from infra.path_handler import *
from infra.setup_logger import *
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_directory()
    await connect_database()

    asyncio.create_task(check_changes())
    asyncio.create_task(event_watcher())

    yield
    await disconnect_database()

app = FastAPI(
    debug=True,
    title="charmee",
    version="0.1.6-alpha",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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