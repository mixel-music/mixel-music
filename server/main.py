from routes import albums_api, images_api, stream_api, tracks_api
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tools.path import *
from core.logs import *
from core.scan import *
from model import *
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    #asyncio.create_task(original_scan())
    asyncio.create_task(scan_path())
    # asyncio.create_task(ScanTools.scan_detect())
    yield
    await disconnect_database()

app = FastAPI(
    debug=True,
    title="Tamaya",
    version="0.1.0-a6",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.include_router(stream_api.router, prefix="/api")
app.include_router(tracks_api.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        log_config=None,
        reload=True
    )