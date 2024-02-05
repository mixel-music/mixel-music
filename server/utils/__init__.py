from fastapi import FastAPI, APIRouter, Response, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from mutagen._file import File
from pathlib import Path

from .tools import *
from .tags import *