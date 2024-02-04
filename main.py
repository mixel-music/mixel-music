from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server import stream, tracks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stream.router, prefix="/api")
app.include_router(tracks.router, prefix="/api")