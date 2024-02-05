from utils.modules import *

router = APIRouter()

@router.get("/list")
async def api_list(type: str = 'album'):
    path_list = get_abs_path('test')

    if type == 'album':
        list_album = []
        for ext in valid_ext:
            for album in path_list.rglob(f'*{ext}'):
                _, _, album_name, album_year, _ = await get_music_info(album)
                if not album_name in list_album:
                    list_album.append(album_name)

        return list_album

    elif type == 'songs':
        list_songs = []
        for ext in valid_ext:
            for songs in path_list.rglob(f'*{ext}'):
                songs_name, songs_artist, songs_album, songs_year, _ = await get_music_info(songs)
                path_rel = songs.relative_to(path_list)
                list_songs.append([songs_name, songs_artist, songs_album, songs_year, path_rel])

        return list_songs