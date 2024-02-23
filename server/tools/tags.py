from datetime import datetime
from mutagen import File
from tools.path import *

async def TagsTools(path: Path, tags: list) -> dict:
    tags += 'tracktotal', 'totaldisc', 'totaltracks', 'unsyncedlyrics'
    strpath = get_strpath(path)
    tags_dict = {}

    try: get_tags = File(path)
    except: return None
    if not get_tags: return tags_dict

    for key in tags:
        if key in get_tags:
            if len(get_tags[key]) == 1:
                tags_dict[key] = get_tags[key][0]
            elif len(get_tags[key]) > 1:
                tags_dict[key] = ', '.join(get_tags[key])
        else:
            tags_dict[key] = ''

    tags_dict['albumid'] = get_hash(f"{tags_dict['album']}-{tags_dict['artist']}-{tags_dict['year']}")
    tags_dict['artistid'] = get_hash(tags_dict['artist'])
    tags_dict['bitrate'] = getattr(get_tags.info, 'bitrate', 0)
    tags_dict['channels'] = getattr(get_tags.info, 'channels', 0)
    tags_dict['compilation'] = False if tags_dict['compilation'] == '' else True
    tags_dict['createdate'] = datetime.now()
    tags_dict['dir'] = get_strpath(path.parent)
    tags_dict['discnumber'] = safe_int(tags_dict['discnumber'])
    tags_dict['duration'] = getattr(get_tags.info, 'length', 0.0)
    tags_dict['id'] = get_hash(strpath)
    tags_dict['imageid'] = ''
    tags_dict['path'] = strpath
    tags_dict['mime'] = getattr(get_tags, 'mime', '')[0]
    tags_dict['samplerate'] = getattr(get_tags.info, 'sample_rate', 0)
    tags_dict['size'] = path.stat().st_size
    tags_dict['tracknumber'] = safe_int(tags_dict['tracknumber'])

    if tags_dict['title'] == '':
        if get_name(strpath)[1]:
            tags_dict['title'] = get_name(strpath)[1]
        else:
            tags_dict['title'] = 'Unknown Title'

    if tags_dict['year'] == '':
        if safe_int(tags_dict['date'].split(',')[0]):
            tags_dict['year'] = safe_int(tags_dict['date'].split(',')[0])
        else:
            tags_dict['year'] = 0

    if tags_dict['artist'] == '': tags_dict['artist'] = 'Unknown Artist'
    if tags_dict['album'] == '': tags_dict['album'] = 'Unknown Album'
    if tags_dict['bpm'] == '': tags_dict['bpm'] = 0

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