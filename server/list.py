from utils import *

router = APIRouter()

@router.get("/list")
async def api_list(type: str):
    list_path = get_absolute_path('test')

    # if type == 'album':
    #     return await database.fetch_all(conn.music.select())
    # elif type == 'music':
    #     return await database.fetch_all(conn.music.select())
    # elif type == 'artist':
    #     return await database.fetch_all(music.select())
    # elif type == 'radio':
    #     return await database.fetch_all(music.select())
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    if type == 'album':
        album_list = []
        for extension in valid_extension_list:
            for album in list_path.rglob(f'*{extension}'):
                try:
                    album_tags = ExtractMediaTag.extract_tags(album)
                    album_title, album_year = album_tags.get('album'), album_tags.get('year')
                except:
                    logging.error('Failed to load album list')
                    break
                if not album_title in album_list and album_year is not False:
                    album_list.append(album_title)
        
        logging.debug('Load album list')
        return album_list
    elif type == 'music':
        music_list = []
        for extension in valid_extension_list:
            for music in list_path.rglob(f'*{extension}'):
                try:
                    music_tags = ExtractMediaTag.extract_tags(music)
                    music_title, music_album, music_artist = music_tags.get('title'), music_tags.get('album'), ''.join(music_tags.get('artist'))
                except:
                    logging.error('Failed to load music list')
                    break
                music_path = music.relative_to(list_path)
                music_list.append([music_title, music_album, music_artist, music_path])

        logging.debug('Load music list')
        return music_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)