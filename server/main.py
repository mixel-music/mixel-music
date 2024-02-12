from utils import *

import subprocess
import stream, list

logging.basicConfig(
    filename=get_absolute_path('.log'),
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
    subprocess.Popen(["python", "scan.py"])

@app.on_event("shutdown")
async def shutdown():
    await disconnect_database()

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(get_absolute_path('data') / 'favicon.ico')

app.include_router(stream.router, prefix="/api")
app.include_router(list.router, prefix="/api")