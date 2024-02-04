from server.utils.modules import *

router = APIRouter()

@router.get("/albums")
async def api_albums():
    music_path = os.path.join(await get_root_path(), "test")
    albums_list = []

    for root, dir, files in os.walk(music_path):
        for filename in files:
            if (await get_split_path(filename))[1] in valid_ext:
                relpath = os.path.relpath(os.path.join(root, filename), await get_root_path())
                _, artist, album, _, _ = await music_metadata(relpath)
                if not album in albums_list:
                    albums_list.append(album)

    return albums_list