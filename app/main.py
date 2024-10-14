from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncio
import toml

from api import (
    albums, artists, artworks, auth, ping, streaming, tracks
)
from core.config import *
from core.database import *
from core.logging import *
from core.middleware import *
from services.scanner import scanner, tracker
from tools.path_handler import create_dir


with open('pyproject.toml') as f:
    pyproject = toml.load(f)
    VERSION = pyproject['tool']['poetry']['version']


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_dir(Config)
    log = log_file_handler()
    await connect_database()

    asyncio.create_task(scanner())
    asyncio.create_task(tracker())

    try:
        yield
    finally:
        await disconnect_database()
        log.close()

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception) and not isinstance(result, asyncio.CancelledError):
                logs.error(f"Error During Shutdown, {result}")


app = FastAPI(
    title='mixel-music',
    debug=Config.DEBUG,
    version=VERSION,
    lifespan=lifespan,
    docs_url=None,
)


if Config.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from fastapi.responses import FileResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from tools.path_handler import get_path


@app.get("/docs", include_in_schema=False)
async def custom_swagger_docs() -> HTMLResponse:
    """
    Apply favicon and dark theme for swagger docs.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f'API • {app.title}',
        swagger_css_url='https://cdn.jsdelivr.net/gh/mixel-music/swagger-ui-dark/dark.css',
        swagger_favicon_url='/favicon.ico',
    )


@app.get('/favicon.ico', include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(get_path('assets', 'favicon.ico'))


app.include_router(albums.router, tags=['Library'])
app.include_router(artists.router, tags=['Library'])
app.include_router(artworks.router, tags=['Library'])
app.include_router(streaming.router, tags=['Library'])
app.include_router(tracks.router, tags=['Library'])

app.include_router(ping.router, tags=['Server'])
app.include_router(auth.router, tags=['Auth'])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level=Config.LOGLEVEL,
        log_config=None,
    )
