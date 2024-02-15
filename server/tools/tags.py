from mutagen import File
from datetime import datetime
from .path import *
import mutagen
import logging

def safe_int(value: int) -> int:
    try:
        return int(value)
    except ValueError:
        return 0

def TagsTools(music_path: Path, list_tags: list) -> dict:
    rel_path = PathTools.get_path(music_path)
    get_tags = mutagen.File(music_path)
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
            tags_dict[key] = PathTools.get_id(rel_path)

    if tags_dict['compilation'] == '':
        tags_dict['compilation'] = False
    else:
        tags_dict['compilation'] = True

    tags_dict['discnumber'] = safe_int(tags_dict['discnumber'])
    tags_dict['tracknumber'] = safe_int(tags_dict['tracknumber'])

    if tags_dict['title'] == '': tags_dict['title'] = PathTools.file_names(rel_path)[1]
    if tags_dict['artist'] == '': tags_dict['artist'] = 'Unknown Artist'
    if tags_dict['album'] == '': tags_dict['album'] = 'Unknown Album'
    if tags_dict['year'] == '': tags_dict['year'] = 0
    if tags_dict['bpm'] == '': tags_dict['bpm'] = 0

    tags_dict['createdate'] = datetime.now()
    tags_dict['albumid'] = PathTools.get_id(tags_dict['album'])
    tags_dict['artistid'] = PathTools.get_id(tags_dict['artist'])

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

#     if tags_dict['year'] == None and  
            
#     return tags_dict

# """
#     file_tags = [
#         "album",
#         "albumid",
#         "albumsort",
#         "albumartist",
#         "albumartistsort",
#         "artist",
#         "artistid",
#         "artistsort",
#         "barcode",
#         "bitrate",
#         "bpm",
#         "catalognumber",
#         "channels",
#         "comment",
#         "compilation",
#         "composer",
#         "composersort",
#         "conductor",
#         "contentgroup",
#         "copyright",
#         "createdate",
#         "date",
#         "description",
#         "discnumber",
#         "disctotal",
#         "duration",
#         "genre",
#         "grouping",
#         "id",
#         "involved_people",
#         "isrc",
#         "label",
#         "language",
#         "lyricist",
#         "lyrics", 
#         "mime",
#         "mix_artist",
#         "musicbrainz_albumartistid",
#         "musicbrainz_albumid",
#         "musicbrainz_albumtype",
#         "musicbrainz_artistid",
#         "musicbrainz_discid", 
#         "musicbrainz_originalalbumid",
#         "musicbrainz_originalartistid",
#         "musicbrainz_releasegroupid",
#         "musicbrainz_releasetrackid",
#         "musicbrainz_trackid",
#         "orignalalbum",
#         "orignalartist",
#         "orignallyricist",
#         "orignalyear",
#         "path",
#         "publisher",
#         "releasetype",
#         "releasetime",
#         "samplerate",
#         "script",
#         "setsubtitle",
#         "size",
#         "subtitle",
#         "title",
#         "titlesort",
#         "tracknumber",
#         "tracktotal",
#         "year"
#     ]
# """