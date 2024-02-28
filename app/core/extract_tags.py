from mutagen import File, MutagenError
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4, MP4FreeForm
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.asf import ASF
from datetime import datetime

from core.convert_tools import *
from infra.convert_image import *
from infra.path_handler import *

import asyncio

FULL_SUPPORT = ['.mp3', '.mp4', '.m4a', '.aac', '.wav', '.flac']
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
    ('TMED', 'T=50 ORIGINAL_MEDIA_TYPE', 'TXXX:MEDIA', 'media', '----:com.apple.iTunes:MEDIA'): 'media',
    # ('TXXX:MEDIA', 'media', '----:com.apple.iTunes:MEDIA'): 'media',
    # ('TMED', 'T=50 ORIGINAL_MEDIA_TYPE'): 'mediatype',
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
    ('TOR', 'TDOR', 'T=30', 'WM/OriginalReleaseYear', '----:com.apple.iTunes:ORIGYEAR', 'TXXX:ORIGINALYEAR', 'originalyear', '----:com.apple.iTunes:ORIGINALYEAR'): 'originalyear',
    # ('TXXX:ORIGINALYEAR', 'originalyear', '----:com.apple.iTunes:ORIGINALYEAR'): 'originalyear',
    ('TOLY', 'T=30', 'WM/OriginalLyricist', '----:com.apple.iTunes:ORIGLYRICIST'): 'origlyricist',
    # ('TOR', 'TDOR', 'T=30', 'WM/OriginalReleaseYear', '----:com.apple.iTunes:ORIGYEAR'): 'origyear',
    ('TPUB', '©pub', 'T=30', 'WM/Publisher', 'organization'): 'publisher',
    ('TXXX:RELEASESTATUS', 'releasestatus', '----:com.apple.iTunes:RELEASESTATUS'): 'releasestatus',
    ('TXXX:RELEASETYPE', 'releasetype', '----:com.apple.iTunes:RELEASETYPE'): 'releasetype',
    ('TXXX:SCRIPT', 'script', '----:com.apple.iTunes:SCRIPT'): 'script',
    ('TXXX:SETSUBTITLE', 'TSST', 'T=50 SUBTITLE', '----:com.apple.iTunes:SETSUBTITLE'): 'setsubtitle',
    ('TIT3', 'T=30', 'WM/SubTitle', '----:com.apple.iTunes:SUBTITLE'): 'subtitle',
    ('TIT2', '©nam', 'T=30', 'Title', 'INAM'): 'title',
    ('TSOT', 'sonm', 'T=30 SORT_WITH', 'WM/TitleSortOrder'): 'titlesort',
    ('TRCK', 'trkn', 'T=30 PART_NUMBER', 'WM/TrackNumber', 'ITRK', 'tracknumber'): 'track',
    ('TXXX:TRACKTOTAL', 'tracktotal', '----:com.apple.iTunes:TRACKTOTAL'): 'tracktotal',
    ('USLT', '©lyr', 'T=30 LYRICS', 'WM/Lyrics'): 'unsyncedlyrics',
    ('TXXX:TOTALDISCS', 'totaldiscs'): 'totaldiscs',
    ('TXXX:TOTALTRACKS', 'totaltracks'): 'totaltracks',
    ('TDRC', 'TYER', '©day', 'T=50 DATE_RECORDED', 'WM/Year', 'ICRD'): 'year',
}

class ExtractTags:
    def __init__(self, path: str):
        self.path = path
        self.real_path = get_path(path)
        self.tags_dict = {}
        self.suffix = get_filename(path)[2]

    async def extract_tags(self, rows: list) -> dict:
        try:
            if get_filename(self.path)[2] in FULL_SUPPORT:
                tags = File(self.real_path, easy=False)
                if not tags: return self.tags_dict
                for key, value in tags.items():
                    # ID3, WAV, FLAC
                    if isinstance(value, list) and not isinstance(value[0], MP4FreeForm):
                        sanitize_key = key.split('::')[0]
                        if key.startswith("TXXX:"): sanitize_key = key[5:]
                        self.tags_dict[MAPPING_DICT.get(sanitize_key, sanitize_key)] = list_join(value)
                    # MP4
                    elif isinstance(value, list) and all(isinstance(item, MP4FreeForm) for item in value):
                        str_value = ', '.join(item.decode('utf-8') if isinstance(item, bytes) else str(item) for item in value)
                        key = key[len('----:com.apple.iTunes:'):] if key.startswith('----:com.apple.iTunes:') else key
                        self.tags_dict[MAPPING_DICT.get(key, key)] = str_value
            else:
                tags = File(self.real_path, easy=True)
                if not tags: return self.tags_dict
                for key, value in tags.items(): self.tags_dict[key] = value

        except MutagenError as error:
            logs.error("Failed to initialize mutagen, %s", error)
            return self.tags_dict

        self.tags_dict.update({
            'album': self.tags_dict.get('album', 'Unknown Album'),
            'albumid': get_hash_str(self.tags_dict.get('album', 'Unknown Album')),
            'artist': self.tags_dict.get('artist', 'Unknown Artist'),
            'artistid': get_hash_str(self.tags_dict.get('artist', 'Unknown Artist')),
            'bitrate': getattr(tags.info, 'bitrate', 0),
            'bpm': int(self.tags_dict.get('bpm', 0)),
            'channels': getattr(tags.info, 'channels', 0),
            'create_date': datetime.now(),
            'directory': str_path(self.real_path.parent),
            'duration': getattr(tags.info, 'length', 0.0),
            'id': get_hash_str(self.path),
            'mime': getattr(tags, 'mime', [''])[0],
            'path': self.path,
            'samplerate': getattr(tags.info, 'sample_rate', 0),
            'size': self.real_path.stat().st_size,
            'update_date': datetime.now(),
        })

        self.tags_dict['compilation'] = False if not self.tags_dict.get('compilation') else True
        self.tags_dict['discnumber'] = sanitize_num(self.tags_dict.get('discnumber', 0))
        self.tags_dict['disctotal'] = max(sanitize_num(self.tags_dict.get('disctotal', 0)), sanitize_num(self.tags_dict.pop('totaldiscs', 0)))
        self.tags_dict['lyrics'] = self.tags_dict.pop('unsyncedlyrics', self.tags_dict.get('lyrics', ''))
        self.tags_dict['title'] = self.tags_dict.get('title', get_filename(self.path)[1] if get_filename(self.path)[1] else 'Unknown Title')
        self.tags_dict['tracknumber'] = max(sanitize_num(self.tags_dict.get('track', 0)), sanitize_num(self.tags_dict.pop('tracknumber', 0)))
        self.tags_dict['tracktotal'] = max(sanitize_num(self.tags_dict.get('tracktotal', 0)), sanitize_num(self.tags_dict.pop('totaltracks', 0)))

        date_result, date_raw = None, self.tags_dict.get('date', '')
        year_result, year_raw = None, self.tags_dict.get('year', '')

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

        self.tags_dict['date'] = date_result
        self.tags_dict['year'] = year_result

        # print(self.tags_dict)

        image_data = await self._extract_image()
        if image_data:
            self.tags_dict['imageid'] = hashlib.md5(image_data).hexdigest().upper()
            asyncio.create_task(convert_image(image_data))
        else:
            self.tags_dict['imageid'] = ''

        self.tags_dict = {key: self.tags_dict.get(key, '') for key in rows}
        return dict(sorted(self.tags_dict.items()))
    
    async def _extract_image(self):
        if self.suffix == '.mp3':
            track_tags = ID3(self.real_path)
            for tag in track_tags.values():
                return tag.data if isinstance(tag, APIC) else None
            
        elif self.suffix in ['.mp4', '.m4a', '.aac']:
            track_tags = MP4(self.real_path)
            covers = track_tags.get('covr')
            
            return covers[0] if covers else None
        
        elif self.suffix == '.flac':
            track_tags = FLAC(self.real_path)
            for picture in track_tags.pictures:
                return picture.data if picture.type == 3 else None
            
        elif self.suffix == '.alac':
            track_tags = MP4(self.real_path)
            covers = track_tags.tags.get('covr')

            return covers[0].data if covers else None
        
        elif self.suffix == '.wma':
            track_tags = ASF(self.real_path)
            if 'WM/Picture' in track_tags.asf_tags:
                pictures = track_tags.asf_tags['WM/Picture']

                return pictures[0].value.data if pictures else None
            
        elif self.suffix == '.aiff':
            track_tags = AIFF(self.real_path)
            if track_tags.tags is None: pass
            id3 = ID3(self.real_path)
            for tag in id3.values():
                return tag.data if isinstance(tag, APIC) else None