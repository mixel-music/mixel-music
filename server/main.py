from routes import albums, artists, images, playlists, stream, tracks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from model.database import *
from model.logger import *
from model.scan import *
from tools.path import *
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    try:
        asyncio.create_task(ScanTools.manual_scan())
        asyncio.create_task(ScanTools.folder_scan())
    except KeyboardInterrupt:
        pass
    yield
    await disconnect_database()

app = FastAPI(
    debug=True,
    title="Tamaya",
    version="0.1.0a",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.include_router(stream.router, prefix="/api")
app.include_router(tracks.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        log_config=None,
        reload=True
    )