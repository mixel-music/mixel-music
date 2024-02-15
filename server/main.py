from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import stream
from core import *
import asyncio

logging.basicConfig(
    filename=PathTools.abs_path('conf', '.log'),
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
    asyncio.create_task(scan())

@app.on_event("shutdown")
async def shutdown():
    await disconnect_database()
    
app.include_router(stream.router, prefix="/api")