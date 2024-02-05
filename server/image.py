from utils import *

router = APIRouter()

@router.get("/image")
async def api_list(type: str = 'album'):
    path_list = get_abs_path('test')

    #TODO: check performance issue

    if type == 'album':
        list_album = []
        for ext in valid_ext:
            for album in path_list.rglob(f'*{ext}'):
                try:
                    data = extract_metadata(album)
                    name, year = data.m_album(), data.m_release()
                except:
                    break

                if not name in list_album and name is not False:
                    list_album.append(name)

        return list_album

    elif type == 'songs':
        list_songs = []
        for ext in valid_ext:
            for songs in path_list.rglob(f'*{ext}'):
                try:
                    data = extract_metadata(songs)
                    title, album, artist, year = data.m_title(), data.m_album(), data.m_artists(), data.m_release()
                except:
                    break

                path_rel = songs.relative_to(path_list)
                list_songs.append([title, album, artist, year, path_rel])

        return list_songs