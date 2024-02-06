from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.func import *
import stream, list, scan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(get_abs_path('data') / 'favicon.ico')

app.include_router(stream.router, prefix="/api")
app.include_router(list.router, prefix="/api")
app.include_router(scan.router, prefix="/api")