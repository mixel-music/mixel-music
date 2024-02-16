from routes import stream, tracks, albums, artists, playlists
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from model.database import *
from model.scan import *
from tools.path import *

logging.basicConfig(
    filename=PathTools.abs('data', '.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await connect_database()
    try:
        asyncio.create_task(ScanTools.manual_scan())
        asyncio.create_task(ScanTools.change_scan())
    except KeyboardInterrupt:
        pass

@app.on_event("shutdown")
async def shutdown():
    await disconnect_database()
    
app.include_router(stream.router, prefix="/api")
app.include_router(tracks.router, prefix="/api")