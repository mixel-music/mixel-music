from server.utils.modules import *

router = APIRouter()

@router.get("/tracks")
async def api_tracks():
    music_path = os.path.join(await get_root_path(), "test")
    music_files = []

    for root, dir, files in os.walk(music_path):
        for filename in files:
            if (await get_split_path(filename))[1] in valid_ext:
                relpath = os.path.relpath(os.path.join(root, filename), await get_root_path())
                title, artist, album, year, image = await music_metadata(relpath)
                music_files.append([title, artist, album, year, relpath])

    return music_files