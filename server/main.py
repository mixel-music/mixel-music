from utils import *

import subprocess
import stream, list

DATABASE_URL = "sqlite:///../data/tamaya.db"

logging.basicConfig(
    filename=get_absolute_path('.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if not get_absolute_path('data', 'tamaya.db').exists():
    metadata = sqlalchemy.MetaData()
    music = sqlalchemy.Table(
        "music",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
        sqlalchemy.Column("title", sqlalchemy.String),
        sqlalchemy.Column("album", sqlalchemy.String),
        sqlalchemy.Column("artist", sqlalchemy.String),
        sqlalchemy.Column("year", sqlalchemy.String),
        sqlalchemy.Column("album_artist", sqlalchemy.String),
        sqlalchemy.Column("disc_number", sqlalchemy.Integer),
        sqlalchemy.Column("track_number", sqlalchemy.Integer),
        sqlalchemy.Column("is_compil", sqlalchemy.Boolean),
        sqlalchemy.Column("genre", sqlalchemy.String),
        sqlalchemy.Column("composer", sqlalchemy.String),
        sqlalchemy.Column("comment", sqlalchemy.String),
        sqlalchemy.Column("copyright", sqlalchemy.String),
        sqlalchemy.Column("isrc", sqlalchemy.String),
        sqlalchemy.Column("lyrics", sqlalchemy.String),
        sqlalchemy.Column("length", sqlalchemy.Integer),
        sqlalchemy.Column("bitrate", sqlalchemy.Integer),
        sqlalchemy.Column("channels", sqlalchemy.Integer),
        sqlalchemy.Column("sample_rate", sqlalchemy.Integer),
        sqlalchemy.Column("mime", sqlalchemy.String),
    )
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    logging.debug("Creating DB Tables...")

    database = Database(DATABASE_URL)
    logging.debug("Connected! %s", DATABASE_URL)
else:
    database = Database(DATABASE_URL)
    logging.debug("Connected! (Skipped create_all tasks) %s", DATABASE_URL)

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
    await database.connect()
    subprocess.Popen(["python", "scan.py"])

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(get_absolute_path('data') / 'favicon.ico')

app.include_router(stream.router, prefix="/api")
app.include_router(list.router, prefix="/api")