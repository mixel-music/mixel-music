from datetime import datetime
from mutagen import File
from tools.path import *

# 코드 모듈화 및 갈아 엎을 필요 있음

def safe_int(value: int) -> int:
    try:
        return int(value)
    except ValueError:
        return 0

async def TagsTools(music_path: Path, list_tags: list) -> dict:
    rel_path = get_strpath(music_path)

    try:
        get_tags = File(music_path)
    except:
        return None
    
    tags_dict = {}

    if not get_tags:
        return tags_dict

    list_tags += 'tracktotal', 'totaldisc', 'totaltracks', 'unsyncedlyrics'

    for key in list_tags:
        if key in get_tags:
            if len(get_tags[key]) == 1:
                tags_dict[key] = get_tags[key][0]
            else:
                tags_dict[key] = ', '.join(get_tags[key])
        else:
            tags_dict[key] = ''

        if key == "size":
            tags_dict[key] = music_path.stat().st_size
        elif key == "duration":
            tags_dict[key] = getattr(get_tags.info, 'length', 0.0)
        elif key == "bitrate":
             tags_dict[key] = getattr(get_tags.info, 'bitrate', 0)
        elif key == "channels":
            tags_dict[key] = getattr(get_tags.info, 'channels', 0)
        elif key == "samplerate":
            tags_dict[key] = getattr(get_tags.info, 'sample_rate', 0)
        elif key == "mime":
            tags_dict[key] = getattr(get_tags, 'mime', '')[0]
        elif key == "path":
            tags_dict[key] = rel_path
        elif key == "id":
            tags_dict[key] = get_hash(rel_path)

    if tags_dict['compilation'] == '':
        tags_dict['compilation'] = False
    else:
        tags_dict['compilation'] = True

    tags_dict['dir'] = get_strpath(music_path.parent)        
    tags_dict['discnumber'] = safe_int(tags_dict['discnumber'])
    tags_dict['tracknumber'] = safe_int(tags_dict['tracknumber'])
    tags_dict['imageid'] = ' '

    if tags_dict['title'] == '': tags_dict['title'] = get_name(rel_path)[1]
    if tags_dict['artist'] == '': tags_dict['artist'] = 'Unknown Artist'
    if tags_dict['album'] == '': tags_dict['album'] = 'Unknown Album'
    if tags_dict['year'] == '': tags_dict['year'] = 0
    if tags_dict['bpm'] == '': tags_dict['bpm'] = 0

    tags_dict['createdate'] = datetime.now()
    tags_dict['albumid'] = get_hash(tags_dict['album'])
    tags_dict['artistid'] = get_hash(tags_dict['artist'])

    lyrics_value = tags_dict['lyrics'] or tags_dict['unsyncedlyrics']
    tags_dict['lyrics'] = lyrics_value[0] if isinstance(lyrics_value, list) else lyrics_value or {}
    tags_dict.pop('unsyncedlyrics')

    disc_values = [safe_int(tags_dict['disctotal']), safe_int(tags_dict['totaldisc'])]
    tags_dict['disctotal'] = max(disc_values) if any(disc_values) else 0
    tags_dict.pop('totaldisc')

    track_values = [safe_int(tags_dict['tracktotal']), safe_int(tags_dict['totaltracks'])]
    tags_dict['tracktotal'] = max(track_values) if any(track_values) else 0
    tags_dict.pop('totaltracks')

    return tags_dict