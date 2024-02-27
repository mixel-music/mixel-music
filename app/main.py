from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import uvicorn

from api import images_api, stream_api, tracks_api
from core.library_changes import *
from infra.database import *
from infra.init_logger import *
from infra.handle_path import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_directory()
        await connect_database()
        asyncio.create_task(check_changes())
        asyncio.create_task(event_watcher())

    except KeyboardInterrupt:
        for task in asyncio.all_tasks():
            task.cancel()
    yield
    for task in asyncio.all_tasks():
        task.cancel()
    await disconnect_database()

app = FastAPI(
    debug=True,
    title="charmee",
    version="0.1.5-alpha",
    lifespan=lifespan
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
        reload=True
    )