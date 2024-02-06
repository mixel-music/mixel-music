from utils import *

router = APIRouter()

@router.get("/list")
async def api_list(type: str = 'album'):
    list_path = get_abs_path('test')

    if type == 'album':
        list_album = []
        tag = {}
        for ext in valid_ext:
            for album in list_path.rglob(f'*{ext}'):
                try:
                    tags = audio_tags(album)
                    album_title, album_year = tags.get('album'), tags.get('year')
                except:
                    break

                if not album_title in list_album and album_year is not False:
                    list_album.append(album_title)

        return list_album

    elif type == 'music':
        list_music = []
        tag = {}
        for ext in valid_ext:
            for music in list_path.rglob(f'*{ext}'):
                try:
                    tags = audio_tags(music)
                    music_title, music_album, music_artist, music_year = tags.get('title'), tags.get('album'), ''.join(tags.get('artist')), (tags.get('year'))[0]
                except:
                    break

                music_path = music.relative_to(list_path)
                list_music.append([music_title, music_album, music_artist, music_year, music_path])

        return list_music