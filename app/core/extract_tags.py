from mutagen import File, MutagenError
from mutagen.mp4 import MP4FreeForm
from datetime import datetime
from core.convert_data import *
from infra.handle_path import *
import filetype

# async def extract_tags(path: str | Path) -> dict:
#     path = get_path(path)
#     tags_list = {}

#     try:
#         get_tags = File(path)
#         if not get_tags: return tags_list
#     except MutagenError:
#         return tags_list
    
#     for tag in get_tags:
#         tags_list[tag] = get_tags[tag]

#     print(sorted(tags_list.keys()))

#     return tags_list.keys()

# For ID3, FLAC, MP4, WAV, WMA: Advanced tag extraction
MAPPING_DICT = {
    ('TALB', '©alb', 'T=50 TITLE', 'WM/AlbumTitle', 'IPRD'): 'album',
    ('TSOA', 'soal', 'T=50 SORT_WITH', 'WM/AlbumSortOrder'): 'albumsort',
    ('TPE2', 'aART', 'T=50 ARTIST', 'WM/AlbumArtist'): 'albumartist',
    ('TSO2', 'soaa', 'T=30'): 'albumartistsort',
    ('TPE1' '©art' 'T=30' 'ARTIST' 'Author' 'IART'): 'artist',
    ('TXXX:ARTISTS', 'artists', '----:com.apple.iTunes:ARTISTS'): 'artists',
    ('TSOP', 'soar', 'T=30', 'WM/ArtistSortOrder'): 'artistsort',
    ('TXXX:BARCODE', '----:com.apple.iTunes:BARCODE', 'T=30', 'WM/Barcode'): 'barcode',
    ('TBPM', 'tmpo', 'T=30', 'WM/BeatsPerMinute'): 'bpm',
    ('TXXX:CATALOGNUMBER', '----:com.apple.iTunes:CATALOGNUMBER', 'T=30', 'WM/CatalogNo'): 'catalognumber',
    ('COMM', '©cmt', 'T=30', 'Description', 'ICMT'): 'comment',
    ('TCMP', 'cpil' 'T=30'): 'compilation',
    ('TCOM', '©wrt', 'T=30', 'WM/Composer'): 'composer',
    ('TSOC', 'soco', 'T=30'): 'composersort',
    ('TPE3', '©con', 'T=30', 'WM/Conductor'): 'conductor',
    ('TIT1', '©grp', 'T=30', 'WM/ContentGroupDescription'): 'contentgroup',
    ('TCOP', 'cprt', 'T=30', 'Copyright', 'ICOP'): 'copyright',
    ('TDAT', 'TXXX:DATE'): 'date',
    ('desc', 'T=30'): 'description',
    ('TXXX:DIRECTOR', 'director', '©dir'): 'director',
    ('TPOS', 'disk', 'T=50 PART_NUMBER', 'WM/PartOfSet'): 'discnumber',
    ('TXXX:DISCTOTAL', 'disctotal', '----:com.apple.iTunes:DISCTOTAL'): 'disctotal',
    ('TCON', '©gen', 'T=30', 'WM/Genre', 'IGNR'): 'genre',
    ('GRP1', 'T=30', '----:com.apple.iTunes:GROUPING'): 'grouping',
    ('TSRC', '----:com.apple.iTunes:ISRC', 'T=30', 'WM/ISRC'): 'isrc',
    ('TXXX:LABEL', 'label', '----:com.apple.iTunes:LABEL'): 'label',
    ('TLAN', 'T=30', 'WM/Language', 'ILNG', '----:com.apple.iTunes:LANGUAGE'): 'language',
    ('TEXT', 'T=30', '----:com.apple.iTunes:LYRICIST'): 'lyricist',
    ('TXXX:LYRICS', 'lyrics'): 'lyrics',
    ('TXXX:MEDIA', 'media', '----:com.apple.iTunes:MEDIA'): 'media',
    ('TMED', 'T=50 ORIGINAL_MEDIA_TYPE'): 'mediatype',
    ('TPE4', 'T=30 REMIXED_BY', '----:com.apple.iTunes:MIXARTIST'): 'mixartist',
    ('TXXX:MusicBrainz Album Artist Id', '----:com.apple.iTunes:MusicBrainz Album Artist Id'): 'musicbrainz_albumartistid',
    ('TXXX:MusicBrainz Album Id', '----:com.apple.iTunes:MusicBrainz Album Id'): 'musicbrainz_albumid',
    ('TXXX:MusicBrainz Album Release Country', '----:com.apple.iTunes:MusicBrainz Album Release Country'): 'musicbrainz_albumreleasecountry',
    ('TXXX:MusicBrainz Album Status', '----:com.apple.iTunes:MusicBrainz Album Status'): 'musicbrainz_albumstatus',
    ('TXXX:MusicBrainz Album Type', '----:com.apple.iTunes:MusicBrainz Album Type'): 'musicbrainz_albumtype',
    ('TTXXX:MusicBrainz Artist Id', '----:com.apple.iTunes:MusicBrainz Artist Id'): 'musicbrainz_artistid',
    ('TTXXX:MusicBrainz Disc Id', '----:com.apple.iTunes:MusicBrainz Disc Id'): 'musicbrainz_discid',
    ('TXXX:MusicBrainz Original Album Id', '----:com.apple.iTunes:MusicBrainz Original Album Id'): 'musicbrainz_originalalbumid',
    ('TXXX:MusicBrainz Original Artist Id', '----:com.apple.iTunes:MusicBrainz Original Artist Id'): 'musicbrainz_originalartistid',
    ('TXXX:MusicBrainz Release Group Id', '----:com.apple.iTunes:MusicBrainz Release Group Id'): 'musicbrainz_releasegroupid',
    ('TTXXX:MusicBrainz Release Track Id', '----:com.apple.iTunes:MusicBrainz Release Track Id'): 'musicbrainz_releasetrackid',
    ('UFID:http://musicbrainz.org', '----:com.apple.iTunes:MusicBrainz Track Id'): 'musicbrainz_trackid',
    ('TOAL', 'T=30', 'WM/OriginalAlbumTitle', '----:com.apple.iTunes:ORIGALBUM'): 'origalbum',
    ('TOPE', 'T=30', 'WM/OriginalArtist', '----:com.apple.iTunes:ORIGARTIST'): 'origartist',
    ('TXXX:ORIGINALDATE', 'originaldate'): 'originaldate',
    ('TXXX:ORIGINALYEAR', 'originalyear', '----:com.apple.iTunes:ORIGINALYEAR'): 'originalyear',
    ('TOLY', 'T=30', 'WM/OriginalLyricist', '----:com.apple.iTunes:ORIGLYRICIST'): 'origlyricist',
    ('TOR', 'TDOR', 'T=30', 'WM/OriginalReleaseYear', '----:com.apple.iTunes:ORIGYEAR'): 'origyear',
    ('TXXX:RELEASESTATUS', 'releasestatus', '----:com.apple.iTunes:RELEASESTATUS'): 'releasestatus',
    ('TXXX:RELEASETYPE', 'releasetype', '----:com.apple.iTunes:RELEASETYPE'): 'releasetype',
    ('TXXX:SCRIPT', 'script', '----:com.apple.iTunes:SCRIPT'): 'script',
    ('TPUB', '©pub', 'T=30', 'WM/Publisher', 'organization'): 'publisher',
    ('TXXX:SETSUBTITLE', 'TSST', 'T=50 SUBTITLE', '----:com.apple.iTunes:SETSUBTITLE'): 'setsubtitle',
    ('TIT3', 'T=30', 'WM/SubTitle', '----:com.apple.iTunes:SUBTITLE'): 'subtitle',
    ('TIT2', '©nam', 'T=30', 'Title', 'INAM'): 'title',
    ('TSOT', 'sonm', 'T=30 SORT_WITH', 'WM/TitleSortOrder'): 'titlesort',
    ('TRCK', 'trkn', 'T=30 PART_NUMBER', 'WM/TrackNumber', 'ITRK'): 'tracknumber',
    ('TXXX:TRACKTOTAL', 'tracktotal', '----:com.apple.iTunes:TRACKTOTAL'): 'tracktotal',
    ('USLT', '©lyr', 'T=30 LYRICS', 'WM/Lyrics'): 'unsyncedlyrics',
    ('TXXX:TOTALDISCS', 'totaldiscs'): 'totaldiscs',
    ('TXXX:TOTALTRACKS', 'totaltracks'): 'totaltracks',
    ('TDRC', 'TYER', '©day', 'T=50 DATE_RECORDED', 'WM/Year', 'ICRD'): 'year',
}

def sanitize_value(value):
    if isinstance(value, list):
        return ', '.join(str(item) for item in value)
    return str(value)

async def extract_tags(path: str) -> dict:
    real_path = get_path(path)
    tags_dict = {}

    try:
        tags = File(path)
        if not tags: return tags_dict
    except MutagenError:
        return tags_dict

    for key, value in tags.items():
        # ID3, WAV, FLAC
        if not isinstance(value, list) or (isinstance(value, list) and not isinstance(value[0], MP4FreeForm)):
            sanitize_key = key.split('::')[0]
            if key.startswith("TXXX:"):
                sanitize_key = key[5:]
            tags_dict[MAPPING_DICT.get(sanitize_key, sanitize_key)] = sanitize_value(value)
        # MP4
        elif isinstance(value, list) and all(isinstance(item, MP4FreeForm) for item in value):
            strvalue = ', '.join(item.decode('utf-8') if isinstance(item, bytes) else str(item) for item in value)
            key = key[len('----:com.apple.iTunes:'):] if key.startswith('----:com.apple.iTunes:') else key
            tags_dict[MAPPING_DICT.get(key, key)] = strvalue

    tags_dict.update({
        'bitrate': getattr(tags.info, 'bitrate', 0),
        'channels': getattr(tags.info, 'channels', 0),
        'duration': getattr(tags.info, 'length', 0.0),
        'sample_rate': getattr(tags.info, 'sample_rate', 0),
        'mime': getattr(tags, 'mime', [''])[0],
        'size': real_path.stat().st_size,
        'directory': str_path(real_path.parent),
        'create_date': datetime.now(),
        'update_date': datetime.now(),
        'path': path,
    })

    tags_dict['id'] = get_hash_str(path)
    tags_dict['albumid'] = get_hash_str(tags_dict.get('album', 'Unknown Album'))
    tags_dict['artistid'] = get_hash_str(tags_dict.get('artist', 'Unknown Artist'))
    tags_dict['imageid'] = ''

    tags_dict['compilation'] = False if not tags_dict.get('compilation') else True
    tags_dict['track'] = sanitize_num(tags_dict.get('track', 0))
    tags_dict['discnumber'] = sanitize_num(tags_dict.get('discnumber', 0))
    tags_dict['disctotal'] = max(sanitize_num(tags_dict.get('disctotal', 0)), sanitize_num(tags_dict.pop('totaldiscs', 0)))
    tags_dict['tracktotal'] = max(sanitize_num(tags_dict.get('tracktotal', 0)), sanitize_num(tags_dict.pop('totaltracks', 0)))

    tags_dict['title'] = tags_dict.get('title', get_filename(path)[1] if get_filename(path)[1] else 'Unknown Title')
    tags_dict['album'] = tags_dict.get('album', 'Unknown Album')
    tags_dict['artist'] = tags_dict.get('artist', 'Unknown Artist')
    tags_dict['bpm'] = int(tags_dict.get('bpm', 0))
    tags_dict['lyrics'] = tags_dict.pop('unsyncedlyrics', tags_dict.get('lyrics', ''))

    date_result = None
    year_result = None

    date_raw = tags_dict.get('date', '')
    year_raw = tags_dict.get('year', '')

    if '-' or '.' or ',' in date_raw:
        date_result = date_raw
        if ',' in date_raw:
            year_result = sanitize_num(date_raw.split(',')[0])
            date_result = date_raw.split(', ')[1]
        elif '-' in date_raw:
            year_result = sanitize_num(date_raw.split('-')[0])
        elif '.' in date_raw:
            year_result = sanitize_num(date_raw.split('.')[0])
    elif date_raw:
        date_result = date_raw

    if not year_result and year_raw:
        year_result = sanitize_num(year_raw)

    tags_dict['date'] = date_result
    tags_dict['year'] = year_result

    return dict(sorted(tags_dict.items()))
