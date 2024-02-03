from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server import play, list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(play.router, prefix="/api")
app.include_router(list.router, prefix="/api")